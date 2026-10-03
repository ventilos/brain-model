#!/usr/bin/env python3
"""Regression tests for BM-A031 Rev2 against BM-A027 Amendment-002."""
from __future__ import annotations
import importlib.util
import tempfile
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RUNNER = REPO / "src" / "BM-A031_G2_PATCHED_RUNNER.py"
if not RUNNER.is_file():
    raise SystemExit(f"BM-A031 canonical verification target not found: {RUNNER}")

spec = importlib.util.spec_from_file_location("bm_a031", RUNNER)
bm = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(bm)


def test_constants():
    assert bm.STATES == ["LL", "LH", "HL", "HH"]
    assert bm.CHECKPOINT_SCHEMA == 3
    assert bm.APPLICABLE_G2_AMENDMENT == "BM-A027-AMENDMENT-002"
    assert "AMENDMENT-002" in bm.PARENT
    assert "V3" in bm.EXECUTION_ID


def test_zero_outgoing_row_is_nan():
    class Base:
        @staticmethod
        def n2_runs(epoch_ids, stages, valid, k4):
            return None, [np.array([0, 1, 0, 2, 3], dtype=int)]
    q, P, n_occ, n_trans = bm.lower_order_from_k4(Base(), None, None, None, None)
    assert n_occ == 5 and n_trans == 4
    assert np.all(np.isnan(P[3]))
    assert np.isclose(q.sum(), 1.0)


def test_finite_only_null_and_no_artificial_row_mismatch():
    qobs = np.array([0.4, 0.3, 0.2, 0.1])
    Pobs = np.array([[0.5,0.5,0,0],[0,1,0,0],[0,0,1,0],[np.nan]*4], float)
    Qnull = np.tile(qobs, (3, 1))
    Pnull = np.array([
        [[0.4,0.6,0,0],[0,1,0,0],[0,0,1,0],[np.nan]*4],
        [[0.6,0.4,0,0],[0,1,0,0],[0,0,1,0],[np.nan]*4],
        [[np.nan,0.5,0,0],[0,1,0,0],[0,0,1,0],[np.nan]*4],
    ], float)
    D_occ, D_self, D_M1, _, pmed = bm.mismatch(qobs, Pobs, Qnull, Pnull)
    assert np.isclose(D_occ, 0.0)
    assert np.isclose(pmed[0,0], 0.5)
    assert np.all(np.isnan(pmed[3]))
    assert np.isclose(D_self, 0.0)
    assert np.isclose(D_M1, 0.0)


def test_undefined_row_reporting():
    Pobs = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[np.nan]*4], float)
    Pnull = np.array([
        [[1,0,0,0],[0,1,0,0],[0,0,1,0],[np.nan]*4],
        [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,0],[0,0,1,0],[np.nan]*4],
    ], float)
    r = bm.undefined_row_report(Pobs, Pnull)
    assert r["observed_undefined_row_mask"] == [False, False, False, True]
    assert r["observed_undefined_row_count"] == 1
    assert np.isclose(r["observed_undefined_row_fraction"], 0.25)
    assert r["null_defined_replicates_by_row"] == [3,3,3,1]
    assert r["null_undefined_replicates_by_row"] == [0,0,0,2]
    assert r["affected_by_undefined_rows"] is True


def test_contract_contains_amendment_and_runner_hash():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td); paths=[]
        for i in range(4):
            p=td/f"f{i}.bin"; p.write_bytes(bytes([i+1])); paths.append(p)
        c=bm.checkpoint_contract("REC","common_phase_run",*paths)
        assert c["state_order"] == ["LL","LH","HL","HH"]
        assert c["applicable_g2_amendment"] == "BM-A027-AMENDMENT-002"
        assert c["g2_runner_sha256"] == bm.sha256_file(RUNNER)
        assert "NaN" in c["undefined_transition_row_policy"]
        assert "finite-only" in c["undefined_transition_row_policy"]


def test_checkpoint_fail_closed_on_contract_mismatch():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"x.resume_v3.npz"
        contract={"analysis_id":bm.ANALYSIS_ID,"applicable_g2_amendment":bm.APPLICABLE_G2_AMENDMENT}
        Q=np.array([[.25,.25,.25,.25]]); PP=np.zeros((1,4,4),float)
        rng=np.random.default_rng(1)
        bm.save_resume_checkpoint(p,contract,Q,PP,1,rng.bit_generator.state,0,0,0,False)
        ok,why,_=bm.validate_resume_checkpoint(p,{**contract,"applicable_g2_amendment":"WRONG"},expected_n=2)
        assert not ok and why == "contract_mismatch"


def test_no_stale_a030_or_schema2_execution_labels():
    text=RUNNER.read_text(encoding="utf-8")
    assert "BM-A030_PLAN_ONLY_PASS" not in text
    assert "BM-A030_CHECKPOINT_SELFTEST_PASS" not in text
    assert "schema 2" not in text


def run_all():
    tests=[v for k,v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        t(); print(f"PASS {t.__name__}")
    print(f"BM-A031_AMENDMENT002_REV2_REGRESSION_PASS tests={len(tests)} runner={RUNNER}")

if __name__ == "__main__": run_all()
