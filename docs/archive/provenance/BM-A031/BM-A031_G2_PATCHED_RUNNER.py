!/usr/bin/env python3
"""BM-A030 -- hardened smart-resume launcher/runner for BM-A029 G2.

Scientific analysis remains BM-A029 / BM-A027 G2. This file changes only the
execution/checkpoint layer. It preserves BM-A011/BM-A029 scientific settings.

Checkpoint design:
- legacy BM-A029/BM-A030 checkpoints are not valid inputs unless they satisfy the full amended V3 contract;
- new checkpoints are single-file atomic NPZ artifacts (schema 2);
- partial state stores Q/PP completed rows + exact NumPy RNG bit-generator state;
- checkpoint is updated every N accepted replay replicates (default 50);
- on restart, a partial recording×variant resumes at the next replicate without
  regenerating earlier completed chunks;
- invalid/stale checkpoints are quarantined fail-closed;
- final G2 aggregation is generated only after all selected recording×variant
  jobs are complete and exact replay checks have passed.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import gzip
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
import uuid

import numpy as np
import pandas as pd
from scipy import stats

ANALYSIS_ID = "BM-A031-G2-LOWER-ORDER-DIAGNOSTICS-PATCHED"
EXECUTION_ID = "BM-A031-G2-SMART-RESUME-CHECKPOINT-V3"
PARENT = "BM-A027 / BM-CHALLENGE-001 + AMENDMENT-001 + AMENDMENT-002"
APPLICABLE_G2_AMENDMENT = "BM-A027-AMENDMENT-002"
R3_ANALYSIS = "BM-A011-ST44-RAW-NULL-V3CS-R3"
B_FROZEN = 1999
SEED_R3 = 20260921
BOOT_B = 10000
BOOT_SEED = 20260929
CHECKPOINT_SCHEMA = 3
DEFAULT_CHUNK = 50
VARIANTS = ["common_phase_run", "independent_channel_phase", "epochwise_common_phase"]
STATES = ["LL", "LH", "HL", "HH"]


def utc_now():
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def sha256_file(p: Path, chunk=8 * 1024 * 1024):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def atomic_write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def atomic_write_json(path: Path, obj):
    atomic_write_text(path, json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + "\n")

def json_safe_array(a):
    """Convert numeric arrays to JSON-safe nested lists; undefined values -> null."""
    a = np.asarray(a, dtype=float)
    def cv(x):
        return float(x) if np.isfinite(x) else None
    if a.ndim == 1:
        return [cv(x) for x in a]
    if a.ndim == 2:
        return [[cv(x) for x in row] for row in a]
    raise ValueError("json_safe_array supports 1D/2D arrays")


def atomic_save_npz(path: Path, **payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.stem}.tmp-{uuid.uuid4().hex}.npz")
    np.savez_compressed(tmp, **payload)
    with open(tmp, "rb") as f:
        os.fsync(f.fileno())
    os.replace(tmp, path)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def lower_order_from_k4(base, epoch_ids, stages, valid, k4):
    """N2 run-local occupancy and first-order transition matrix."""
    _runs, seqs = base.n2_runs(epoch_ids, stages, valid, k4)
    if not seqs:
        raise RuntimeError("No N2 K4 sequences")
    x = np.concatenate(seqs)
    occ = np.bincount(x, minlength=4).astype(float)
    q = occ / occ.sum()
    C = np.zeros((4, 4), dtype=float)
    for s in seqs:
        if len(s) > 1:
            np.add.at(C, (s[:-1], s[1:]), 1.0)
    den = C.sum(axis=1, keepdims=True)
    # BM-A031: a row with no outgoing transitions is undefined, not a zero
    # transition distribution.  Preserve that distinction as NaN.
    P = np.full_like(C, np.nan, dtype=float)
    np.divide(C, den, out=P, where=den > 0)
    return q, P, int(len(x)), int(C.sum())


def _nanmedian_no_warning(a, axis=0):
    """Median over finite values; all-undefined slices remain NaN."""
    a = np.asarray(a, float)
    if axis != 0:
        raise ValueError("BM-A031 helper currently supports axis=0 only")
    out = np.full(a.shape[1:], np.nan, dtype=float)
    for idx in np.ndindex(out.shape):
        vals = a[(slice(None),) + idx]
        vals = vals[np.isfinite(vals)]
        if vals.size:
            out[idx] = np.median(vals)
    return out

def mismatch(qobs, Pobs, Qnull, Pnull):
    qmed = np.median(Qnull, axis=0)
    pmed = _nanmedian_no_warning(Pnull, axis=0)
    D_occ = float(0.5 * np.abs(qobs - qmed).sum())

    # BM-A031 frozen rule: undefined transition rows contribute zero rather
    # than being treated as a zero-probability transition distribution.
    self_obs = np.diag(Pobs)
    self_null = np.diag(pmed)
    valid_self = np.isfinite(self_obs) & np.isfinite(self_null)
    D_self = float(np.sum(qobs[valid_self] * np.abs(self_obs[valid_self] - self_null[valid_self])))

    row_tv = np.zeros(4, dtype=float)
    for i in range(4):
        mask = np.isfinite(Pobs[i]) & np.isfinite(pmed[i])
        if mask.any():
            row_tv[i] = 0.5 * np.abs(Pobs[i, mask] - pmed[i, mask]).sum()
    D_M1 = float(np.sum(qobs * row_tv))
    return D_occ, D_self, D_M1, qmed, pmed


def checkpoint_contract(rec, variant, ref_csv, base_path, prod_path, receipt_path):
    # BM-A031 Amendment-002 contract: code identity, state order, row policy, and amendment ID are mandatory.
    return {
        "analysis_id": ANALYSIS_ID,
        "parent": PARENT,
        "r3_analysis_id": R3_ANALYSIS,
        "recording": rec,
        "variant": variant,
        "B": B_FROZEN,
        "seed_r3": SEED_R3,
        "support": "N2_RUN_LOCAL",
        "g2_runner_sha256": sha256_file(Path(__file__).resolve()),
        "state_order": STATES,
        "applicable_g2_amendment": APPLICABLE_G2_AMENDMENT,
        "undefined_transition_row_policy": "NaN; finite-only null median; undefined observed/null row contributes zero to D_self/D_M1",
        "base_sha256": sha256_file(base_path),
        "prod_sha256": sha256_file(prod_path),
        "receipt_sha256": sha256_file(receipt_path),
        "r3_reference_csv_sha256": sha256_file(ref_csv),
    }


def _np_scalar(z, key):
    x = z[key]
    if isinstance(x, np.ndarray) and x.shape == ():
        return x.item()
    return x


def save_resume_checkpoint(path: Path, contract: dict, Q, PP, next_index: int,
                           rng_state: dict, max_dt: float, max_de: float, max_di: float,
                           complete: bool, final_metrics=None):
    final_metrics = final_metrics or {}
    payload = {
        "checkpoint_schema": np.array(CHECKPOINT_SCHEMA, dtype=np.int64),
        "execution_id": np.array(EXECUTION_ID),
        "contract_json": np.array(json.dumps(contract, sort_keys=True, separators=(",", ":"))),
        "next_index": np.array(int(next_index), dtype=np.int64),
        "complete": np.array(1 if complete else 0, dtype=np.int8),
        "rng_state_json": np.array(json.dumps(rng_state, sort_keys=True, separators=(",", ":"))),
        "Q": np.asarray(Q, dtype=float),
        "PP": np.asarray(PP, dtype=float),
        "max_replay_dT": np.array(float(max_dt)),
        "max_replay_dE": np.array(float(max_de)),
        "max_replay_dI": np.array(float(max_di)),
        "saved_utc": np.array(utc_now()),
        "D_occ": np.array(float(final_metrics.get("D_occ", np.nan))),
        "D_self": np.array(float(final_metrics.get("D_self", np.nan))),
        "D_M1": np.array(float(final_metrics.get("D_M1", np.nan))),
        "qmed": np.asarray(final_metrics.get("qmed", np.empty((0,), float)), dtype=float),
        "pmed": np.asarray(final_metrics.get("pmed", np.empty((0, 0), float)), dtype=float),
    }
    atomic_save_npz(path, **payload)


def validate_resume_checkpoint(path: Path, contract: dict, expected_n=B_FROZEN):
    try:
        with np.load(path, allow_pickle=False) as z:
            if int(_np_scalar(z, "checkpoint_schema")) != CHECKPOINT_SCHEMA:
                return False, "schema_mismatch", None
            got_contract = json.loads(str(_np_scalar(z, "contract_json")))
            if got_contract != contract:
                return False, "contract_mismatch", None
            next_index = int(_np_scalar(z, "next_index"))
            complete = bool(int(_np_scalar(z, "complete")))
            if not (0 <= next_index <= expected_n):
                return False, "next_index_out_of_range", None
            Q = np.asarray(z["Q"], float)
            PP = np.asarray(z["PP"], float)
            if Q.shape != (next_index, 4) or PP.shape != (next_index, 4, 4):
                return False, "shape_mismatch", None
            if not np.isfinite(Q).all():
                return False, "nonfinite_Q", None
            if np.isinf(PP).any():
                return False, "infinite_PP", None
            if next_index and not np.allclose(Q.sum(axis=1), 1.0, atol=1e-10, rtol=0):
                return False, "occupancy_not_normalized", None
            max_dt = float(_np_scalar(z, "max_replay_dT"))
            max_de = float(_np_scalar(z, "max_replay_dE"))
            max_di = float(_np_scalar(z, "max_replay_dI"))
            if max(max_dt, max_de, max_di) > 1e-10:
                return False, "replay_tolerance_exceeded", None
            try:
                rng_state = json.loads(str(_np_scalar(z, "rng_state_json")))
            except Exception:
                return False, "rng_state_invalid", None
            result = {
                "Q": Q,
                "PP": PP,
                "next_index": next_index,
                "complete": complete,
                "rng_state": rng_state,
                "max_replay_dT": max_dt,
                "max_replay_dE": max_de,
                "max_replay_dI": max_di,
            }
            if complete:
                if next_index != expected_n:
                    return False, "complete_but_short", None
                qmed = np.asarray(z["qmed"], float)
                pmed = np.asarray(z["pmed"], float)
                if qmed.shape != (4,) or pmed.shape != (4, 4):
                    return False, "final_metric_shape_mismatch", None
                vals = [float(_np_scalar(z, k)) for k in ["D_occ", "D_self", "D_M1"]]
                if not np.isfinite(vals).all():
                    return False, "final_metrics_nonfinite", None
                result.update({
                    "D_occ": vals[0], "D_self": vals[1], "D_M1": vals[2],
                    "qmed": qmed, "pmed": pmed,
                })
            return True, "complete" if complete else "partial", result
    except Exception as e:
        return False, f"load_error:{type(e).__name__}:{e}", None


def quarantine(path: Path, qroot: Path, reason: str):
    if not path.exists():
        return None
    qdir = qroot / (_dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ") + "_" + uuid.uuid4().hex[:8])
    qdir.mkdir(parents=True, exist_ok=False)
    dst = qdir / path.name
    os.replace(path, dst)
    atomic_write_json(qdir / "QUARANTINE_REASON.json", {"source": str(path), "reason": reason, "timestamp_utc": utc_now()})
    return dst


def import_legacy_complete(legacy_npz: Path, legacy_json: Path, new_path: Path, contract: dict, expected_n=B_FROZEN):
    if not (legacy_npz.exists() and legacy_json.exists()):
        return False, "legacy_absent"
    try:
        if json.loads(legacy_json.read_text(encoding="utf-8")) != contract:
            return False, "legacy_contract_mismatch"
        with np.load(legacy_npz, allow_pickle=False) as z:
            Q = np.asarray(z["Q"], float)
            PP = np.asarray(z["PP"], float)
            if Q.shape != (expected_n, 4) or PP.shape != (expected_n, 4, 4):
                return False, "legacy_shape_mismatch"
            final = {
                "D_occ": float(z["D_occ"]), "D_self": float(z["D_self"]), "D_M1": float(z["D_M1"]),
                "qmed": np.asarray(z["qmed"], float), "pmed": np.asarray(z["pmed"], float),
            }
            max_dt = float(z["max_replay_dT"]); max_de = float(z["max_replay_dE"]); max_di = float(z["max_replay_dI"])
            if max(max_dt, max_de, max_di) > 1e-10:
                return False, "legacy_replay_tolerance_exceeded"
            if not (np.isfinite(Q).all() and np.isfinite(PP).all()):
                return False, "legacy_nonfinite"
        # Full checkpoint never needs RNG state again, but store a valid empty object.
        save_resume_checkpoint(new_path, contract, Q, PP, expected_n, {}, max_dt, max_de, max_di, True, final)
        ok, why, _ = validate_resume_checkpoint(new_path, contract, expected_n)
        return bool(ok), "legacy_imported" if ok else f"legacy_import_validation_failed:{why}"
    except Exception as e:
        return False, f"legacy_load_error:{type(e).__name__}:{e}"


def surrogate_fn(base, variant):
    return {
        "common_phase_run": base.surrogate_common_phase_run,
        "independent_channel_phase": base.surrogate_independent_channel_phase,
        "epochwise_common_phase": base.surrogate_epochwise_common_phase,
    }[variant]


def replay_one_variant_resumable(base, valid, Eobs, Iobs, stages, epoch_ids, raw_runs,
                                  variant, seed, ref, qobs, Pobs, checkpoint_path: Path,
                                  contract: dict, chunk_size: int, qroot: Path,
                                  legacy_npz: Path | None = None, legacy_json: Path | None = None):
    expected_n = len(ref)
    if expected_n != B_FROZEN:
        raise RuntimeError(f"{variant}: expected B={B_FROZEN}, got {expected_n}")

    ok, why, cp = (False, "missing", None)
    if checkpoint_path.exists():
        ok, why, cp = validate_resume_checkpoint(checkpoint_path, contract, expected_n)
        if not ok:
            quarantine(checkpoint_path, qroot, why)
            print(f"{variant}: invalid V2 checkpoint quarantined: {why}", flush=True)

    if not ok and legacy_npz is not None and legacy_json is not None:
        imported, msg = import_legacy_complete(legacy_npz, legacy_json, checkpoint_path, contract, expected_n)
        if imported:
            ok, why, cp = validate_resume_checkpoint(checkpoint_path, contract, expected_n)
            print(f"{variant}: complete legacy BM-A029 checkpoint IMPORTED", flush=True)
        elif msg not in {"legacy_absent", "legacy_contract_mismatch"}:
            print(f"{variant}: legacy checkpoint not reused: {msg}", flush=True)

    if ok and cp["complete"]:
        print(f"{variant}: checkpoint REUSED COMPLETE {expected_n}/{expected_n}", flush=True)
        return cp

    fn = surrogate_fn(base, variant)
    rng = np.random.default_rng(seed)
    if ok and cp is not None and not cp["complete"]:
        Q = np.array(cp["Q"], copy=True)
        PP = np.array(cp["PP"], copy=True)
        start = int(cp["next_index"])
        rng.bit_generator.state = cp["rng_state"]
        max_dt = float(cp["max_replay_dT"]); max_de = float(cp["max_replay_dE"]); max_di = float(cp["max_replay_dI"])
        print(f"{variant}: RESUME PARTIAL at {start}/{expected_n}", flush=True)
    else:
        Q = np.empty((0, 4), dtype=float)
        PP = np.empty((0, 4, 4), dtype=float)
        start = 0
        max_dt = max_de = max_di = 0.0
        print(f"{variant}: START 0/{expected_n}", flush=True)

    ref_reset = ref.reset_index(drop=True)
    for bi in range(start, expected_n):
        row = ref_reset.iloc[bi]
        E = Eobs.copy(); I = Iobs.copy()
        for r, seg in raw_runs:
            if variant == "epochwise_common_phase":
                sur = fn(seg, rng, 3000)
            else:
                sur = fn(seg, rng)
            n = len(r)
            ep = sur.reshape(4, n, 3000).transpose(1, 0, 2)
            ee, mi = base.metrics_for_epochs(ep)
            if not (np.isfinite(ee).all() and np.isfinite(mi).all()):
                raise RuntimeError(f"{variant} replicate {bi+1}: replay produced invalid surrogate")
            E[r] = ee; I[r] = mi
        k4, tx, ty = base.make_k4(E, I, valid, stages, "global")
        T, _ = base.T_n2(epoch_ids, stages, valid, k4)
        dt = abs(float(T) - float(row.T_cs))
        de = abs(float(tx) - float(row.E_threshold))
        di = abs(float(ty) - float(row.ILMI_threshold))
        max_dt = max(max_dt, dt); max_de = max(max_de, de); max_di = max(max_di, di)
        if dt > 1e-10 or de > 1e-10 or di > 1e-10:
            raise RuntimeError(
                f"{variant} replicate {bi+1}: R3 replay mismatch dT={dt:.3g}, dE={de:.3g}, dI={di:.3g}"
            )
        q, p, _, _ = lower_order_from_k4(base, epoch_ids, stages, valid, k4)
        Q = np.concatenate([Q, q[None, :]], axis=0)
        PP = np.concatenate([PP, p[None, :, :]], axis=0)

        done = bi + 1
        if done % chunk_size == 0 or done == expected_n:
            # Save the RNG state AFTER the last completed replicate. Re-entry starts exactly at done.
            if done == expected_n:
                D_occ, D_self, D_M1, qmed, pmed = mismatch(qobs, Pobs, Q, PP)
                final = {"D_occ": D_occ, "D_self": D_self, "D_M1": D_M1, "qmed": qmed, "pmed": pmed}
                save_resume_checkpoint(checkpoint_path, contract, Q, PP, done, rng.bit_generator.state,
                                       max_dt, max_de, max_di, True, final)
            else:
                save_resume_checkpoint(checkpoint_path, contract, Q, PP, done, rng.bit_generator.state,
                                       max_dt, max_de, max_di, False)
            print(f"{variant}: CHECKPOINT {done}/{expected_n}", flush=True)

    ok2, why2, final_cp = validate_resume_checkpoint(checkpoint_path, contract, expected_n)
    if not ok2 or not final_cp["complete"]:
        raise RuntimeError(f"{variant}: final checkpoint validation failed: {why2}")
    return final_cp


def spearman_safe(x, y):
    r = stats.spearmanr(np.asarray(x, float), np.asarray(y, float))
    return float(r.statistic), float(r.pvalue)


def participant_cluster_bootstrap(df, xcol, ycol, B=BOOT_B, seed=BOOT_SEED):
    rng = np.random.default_rng(seed)
    subjects = np.array(sorted(df.subject.unique()))
    vals = []
    for _ in range(B):
        draw = rng.choice(subjects, size=len(subjects), replace=True)
        parts = []
        for j, s in enumerate(draw):
            g = df[df.subject == s].copy()
            g["_boot_cluster"] = j
            parts.append(g)
        bdf = pd.concat(parts, ignore_index=True)
        rho, _ = spearman_safe(bdf[xcol], bdf[ycol])
        if np.isfinite(rho):
            vals.append(rho)
    vals = np.asarray(vals, float)
    return {
        "B_requested": int(B), "B_valid": int(len(vals)), "seed": int(seed),
        "ci95": [float(np.quantile(vals, .025)), float(np.quantile(vals, .975))],
        "median": float(np.median(vals)),
    }


def build_inventory(prod, receipt_path, raw_dir, recordings):
    rr0 = pd.read_csv(receipt_path)
    rr0 = rr0[~rr0.subject_orig.astype(int).isin(prod.PILOT_SUBJECTS)].copy()
    frozen_order = sorted(rr0.recording.astype(str).unique().tolist())
    frozen_index_map = {rec: i for i, rec in enumerate(frozen_order)}
    selected = list(recordings) if recordings else None
    inv = prod.receipt_inventory(receipt_path, raw_dir, recordings=selected, holdout_only=True).reset_index(drop=True)
    inv["frozen_index"] = inv.recording.astype(str).map(frozen_index_map).astype(int)
    if not len(inv):
        raise RuntimeError("No recordings selected")
    return inv


def precompute_resume_plan(inv, r3root, ckroot, legacy_root, base_path, prod_path, receipt_path):
    rows = []
    for _, rr in inv.iterrows():
        rec = str(rr.recording)
        for v in VARIANTS:
            ref_csv = r3root / rec / f"{v}_TCS_NULL.csv"
            contract = checkpoint_contract(rec, v, ref_csv, base_path, prod_path, receipt_path)
            cp_path = ckroot / f"{rec}__{v}.resume_v3.npz"
            if cp_path.exists():
                ok, why, cp = validate_resume_checkpoint(cp_path, contract, B_FROZEN)
                if ok:
                    action = "REUSE_COMPLETE" if cp["complete"] else "RESUME_PARTIAL"
                    progress = int(cp["next_index"])
                else:
                    action = "QUARANTINE_INVALID_RECOMPUTE"
                    progress = 0
            else:
                legacy_npz = legacy_root / f"{rec}__{v}.npz"
                legacy_json = legacy_root / f"{rec}__{v}.json"
                if legacy_npz.exists() and legacy_json.exists():
                    try:
                        legacy_ok = json.loads(legacy_json.read_text(encoding="utf-8")) == contract
                        if legacy_ok:
                            with np.load(legacy_npz, allow_pickle=False) as z:
                                legacy_ok = z["Q"].shape == (B_FROZEN, 4) and z["PP"].shape == (B_FROZEN, 4, 4)
                        action = "IMPORT_LEGACY_COMPLETE" if legacy_ok else "NOT_STARTED"
                        progress = B_FROZEN if legacy_ok else 0
                    except Exception:
                        action = "NOT_STARTED"; progress = 0
                else:
                    action = "NOT_STARTED"; progress = 0
            rows.append({"recording": rec, "variant": v, "action": action, "replay_completed": progress, "B": B_FROZEN})
    return rows


def run(args):
    pkg = Path(args.package_root)
    base_path = pkg / "code" / "BM-A004__CFI_ST44_RAW_SIGNAL_NULL_V3CS_AUDITED.py"
    prod_path = pkg / "code" / "BM-A011__CFI_ST44_RAW_SIGNAL_NULL_V3CS_PRODUCTION.py"
    receipt_path = pkg / "input" / "ST44_DOWNLOAD_RECEIPT.csv"
    base = load_module(base_path, "bm_a004_g2_resume")
    prod = load_module(prod_path, "bm_a011_g2_resume")
    raw_dir = Path(args.raw_dir)
    r3root = Path(args.r3_root)
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    ckroot = out / "CHECKPOINTS_V3"; ckroot.mkdir(exist_ok=True)
    legacy_root = out / "CHECKPOINTS_DISABLED_BY_BM_A031"
    qroot = out / "QUARANTINE_CHECKPOINTS_V3"; qroot.mkdir(exist_ok=True)

    inv = build_inventory(prod, receipt_path, raw_dir, args.recordings)
    plan = precompute_resume_plan(inv, r3root, ckroot, legacy_root, base_path, prod_path, receipt_path)
    plan_payload = {
        "analysis_id": ANALYSIS_ID, "execution_id": EXECUTION_ID, "timestamp_utc": utc_now(),
        "chunk_size": int(args.chunk_size), "jobs_total": len(plan), "B": B_FROZEN,
        "plan": plan,
    }
    atomic_write_json(out / "BM-A031_RESUME_PLAN_CURRENT.json", plan_payload)
    pd.DataFrame(plan).to_csv(out / "BM-A031_RESUME_PLAN_CURRENT.csv", index=False)
    counts = pd.Series([x["action"] for x in plan]).value_counts().to_dict()
    print("RESUME PLAN", counts, flush=True)
    if getattr(args, "plan_only", False):
        print("BM-A030_PLAN_ONLY_PASS", flush=True)
        return

    rows = []; matrices = {}
    complete_keys = {(x["recording"], x["variant"]) for x in plan if x["action"] == "REUSE_COMPLETE"}
    for _, rr in inv.iterrows():
        rec = str(rr.recording); frozen_idx = int(rr.frozen_index)
        print(f"=== {rec} ===", flush=True)
        recdir = r3root / rec
        obs_csv = recdir / "OBSERVED_EPOCH_METRICS.csv"
        summ = json.loads((recdir / "SUMMARY.json").read_text())
        df_saved = pd.read_csv(obs_csv)

        raw, chosen, X, df, valid, Tobs, runs, tx, ty = base.extract_observed(Path(rr.psg), Path(rr.hypnogram))
        if abs(float(Tobs) - float(summ["T_cs_observed"])) > 1e-10:
            raise RuntimeError(f"{rec}: observed T_cs mismatch")
        a = df["K4_state"].fillna("").astype(str).to_numpy()
        b = df_saved["K4_state"].fillna("").astype(str).to_numpy()
        if len(a) != len(b) or not np.array_equal(a, b):
            raise RuntimeError(f"{rec}: observed K4 mismatch against R3 checkpoint")

        Eobs = df.E_eff.to_numpy(float); Iobs = df.ILMI_1s.to_numpy(float)
        stages = df.stage.to_numpy(object); epoch_ids = df.epoch.to_numpy(int)
        kobs = df["K4_state"].fillna("").astype(str).to_numpy(object)
        qobs, Pobs, n_occ, n_trans = lower_order_from_k4(base, epoch_ids, stages, valid, kobs)
        raw_runs = base.build_n2_raw_runs(X, df, runs, 3000)

        matrices[rec] = {"state_order": STATES, "q_obs": json_safe_array(qobs), "P_obs": json_safe_array(Pobs), "n_occ": n_occ, "n_transitions": n_trans}
        for j, v in enumerate(VARIANTS):
            ref_csv = recdir / f"{v}_TCS_NULL.csv"
            ref = pd.read_csv(ref_csv)
            if args.smoke_B is not None:
                # Smoke mode intentionally bypasses persistent production checkpoints.
                ref = ref.head(int(args.smoke_B)).copy()
                # Exact non-resume smoke copied from BM-A029 semantics.
                rng = np.random.default_rng(SEED_R3 + 10007 * frozen_idx + 100000 * j)
                Q = np.empty((0,4),float); PP = np.empty((0,4,4),float)
                fn = surrogate_fn(base, v)
                max_dt=max_de=max_di=0.0
                for bi,rowref in ref.reset_index(drop=True).iterrows():
                    E=Eobs.copy(); I=Iobs.copy()
                    for r,seg in raw_runs:
                        sur = fn(seg,rng,3000) if v=="epochwise_common_phase" else fn(seg,rng)
                        n=len(r); ep=sur.reshape(4,n,3000).transpose(1,0,2)
                        ee,mi=base.metrics_for_epochs(ep); E[r]=ee; I[r]=mi
                    k4,ttx,tty=base.make_k4(E,I,valid,stages,"global"); T,_=base.T_n2(epoch_ids,stages,valid,k4)
                    dt=abs(float(T)-float(rowref.T_cs)); de=abs(float(ttx)-float(rowref.E_threshold)); di=abs(float(tty)-float(rowref.ILMI_threshold))
                    if max(dt,de,di)>1e-10: raise RuntimeError(f"{rec}/{v} smoke mismatch at {bi+1}")
                    max_dt=max(max_dt,dt); max_de=max(max_de,de); max_di=max(max_di,di)
                    q,p,_,_=lower_order_from_k4(base,epoch_ids,stages,valid,k4)
                    Q=np.concatenate([Q,q[None,:]],axis=0); PP=np.concatenate([PP,p[None,:,:]],axis=0)
                D_occ,D_self,D_M1,qmed,pmed=mismatch(qobs,Pobs,Q,PP)
                result={"Q":Q,"PP":PP,"D_occ":D_occ,"D_self":D_self,"D_M1":D_M1,"qmed":qmed,"pmed":pmed,
                        "max_replay_dT":max_dt,"max_replay_dE":max_de,"max_replay_dI":max_di,"complete":True,"next_index":len(ref)}
            else:
                contract = checkpoint_contract(rec, v, ref_csv, base_path, prod_path, receipt_path)
                cp_path = ckroot / f"{rec}__{v}.resume_v3.npz"
                seed = SEED_R3 + 10007 * frozen_idx + 100000 * j
                result = replay_one_variant_resumable(
                    base, valid, Eobs, Iobs, stages, epoch_ids, raw_runs,
                    v, seed, ref, qobs, Pobs, cp_path, contract, int(args.chunk_size), qroot,
                    legacy_root / f"{rec}__{v}.npz", legacy_root / f"{rec}__{v}.json",
                )
                complete_keys.add((rec, v))
                atomic_write_json(out / "BM-A031_PROGRESS_CURRENT.json", {
                    "analysis_id": ANALYSIS_ID, "execution_id": EXECUTION_ID, "timestamp_utc": utc_now(),
                    "jobs_complete": len(complete_keys), "jobs_total": len(inv) * len(VARIANTS),
                    "last_complete": {"recording": rec, "variant": v},
                    "checkpoint_granularity": f"every {int(args.chunk_size)} replay replicates",
                })

            z_T = float(next(x["z_vs_null"] for x in summ["variants"] if x["variant"] == v))
            row = {
                "recording": rec, "subject": int(rr.subject), "night": int(rr.night), "condition": str(rr.condition),
                "variant": v, "support": "N2_RUN_LOCAL", "z_T": z_T,
                "D_occ": float(result["D_occ"]), "D_self": float(result["D_self"]), "D_M1": float(result["D_M1"]),
                "max_replay_dT": float(result["max_replay_dT"]), "max_replay_dE": float(result["max_replay_dE"]),
                "max_replay_dI": float(result["max_replay_dI"]),
            }
            for si, sn in enumerate(STATES):
                row[f"q_obs_{sn}"] = float(qobs[si]); row[f"q_null_median_{sn}"] = float(result["qmed"][si])
                row[f"self_obs_{sn}"] = float(Pobs[si, si]); row[f"self_null_median_{sn}"] = float(result["pmed"][si, si])
            rows.append(row)
            matrices[rec][v] = {
                "state_order": STATES, "q_null_median": json_safe_array(result["qmed"]), "P_null_median": json_safe_array(result["pmed"]),
                "D_occ": float(result["D_occ"]), "D_self": float(result["D_self"]), "D_M1": float(result["D_M1"]),
            }
        del X, raw_runs
        try:
            raw.close()
        except Exception:
            pass

    diag = pd.DataFrame(rows)
    diag_path = out / "BM-A027_LOWER_ORDER_DIAGNOSTICS.csv"
    diag.to_csv(diag_path, index=False)

    summary = {
        "analysis_id": ANALYSIS_ID, "execution_id": EXECUTION_ID, "parent": PARENT, "r3_analysis_id": R3_ANALYSIS,
        "status": "SMOKE_ONLY" if args.smoke_B is not None else "G2_COMPLETE",
        "support": "N2_RUN_LOCAL",
        "implementation_note": "Occupancy and transition matrices are computed on the same N2 run-local K4 support used by T_cs; transitions never cross run boundaries.",
        "B_replayed_per_recording_variant": int(args.smoke_B or B_FROZEN),
        "bootstrap_B": BOOT_B, "bootstrap_seed": BOOT_SEED, "variants": {}, "G1_not_reopened": True,
        "checkpoint_schema": CHECKPOINT_SCHEMA,
        "checkpoint_granularity": None if args.smoke_B is not None else int(args.chunk_size),
    }
    if args.smoke_B is None:
        if len(diag) != len(inv) * len(VARIANTS):
            raise RuntimeError("Final diagnostic row count mismatch")
        for v in VARIANTS:
            d = diag[diag.variant == v].copy(); vd = {}
            for metric in ["D_occ", "D_self", "D_M1"]:
                rho, p = spearman_safe(d["z_T"], d[metric])
                boot = participant_cluster_bootstrap(d, "z_T", metric)
                lop = []
                for s in sorted(d.subject.unique()):
                    dd = d[d.subject != s]; rrho, _ = spearman_safe(dd["z_T"], dd[metric])
                    lop.append({"left_out_subject": int(s), "rho": float(rrho)})
                vd[metric] = {
                    "spearman_rho": rho, "spearman_p_descriptive": p, "cluster_bootstrap": boot,
                    "LOPO_rho_min": float(min(x["rho"] for x in lop)), "LOPO_rho_max": float(max(x["rho"] for x in lop)), "LOPO": lop,
                }
            summary["variants"][v] = vd

    summary_path = out / "BM-A027_LOWER_ORDER_SUMMARY.json"
    atomic_write_json(summary_path, summary)
    matrix_path = out / "BM-A027_LOWER_ORDER_MATRICES.json.gz"
    tmp_gz = matrix_path.with_name(f".{matrix_path.name}.tmp-{uuid.uuid4().hex}")
    with gzip.open(tmp_gz, "wt", encoding="utf-8") as f:
        json.dump(matrices, f, allow_nan=False)
    os.replace(tmp_gz, matrix_path)

    receipt = {
        "analysis_id": ANALYSIS_ID, "execution_id": EXECUTION_ID, "timestamp_utc": utc_now(),
        "g2_runner_sha256": sha256_file(Path(__file__).resolve()),
        "state_order": STATES,
        "applicable_g2_amendment": APPLICABLE_G2_AMENDMENT,
        "undefined_transition_row_policy": "NaN; finite-only null median; undefined observed/null row contributes zero to D_self/D_M1",
        "outputs": {p.name: sha256_file(p) for p in [diag_path, summary_path, matrix_path]},
        "G1_not_reopened": True,
    }
    atomic_write_json(out / "BM-A031_G2_EXECUTION_RECEIPT.json", receipt)
    print(json.dumps(summary, indent=2), flush=True)


def checkpoint_selftest():
    """Proves exact RNG continuation across an atomic partial checkpoint."""
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "selftest.resume_v3.npz"
        contract = {"analysis_id": ANALYSIS_ID, "selftest": True}
        seed = 1234567; n = 23; cut = 7
        r0 = np.random.default_rng(seed)
        full = r0.normal(size=(n, 4))

        r1 = np.random.default_rng(seed)
        q0 = r1.normal(size=(cut, 4)); pp0 = np.zeros((cut, 4, 4), float)
        # Normalize only because validator expects occupancy-like Q rows.
        q0 = np.exp(q0); q0 /= q0.sum(axis=1, keepdims=True)
        save_resume_checkpoint(p, contract, q0, pp0, cut, r1.bit_generator.state, 0, 0, 0, False)
        ok, why, cp = validate_resume_checkpoint(p, contract, n)
        if not ok or cp["next_index"] != cut:
            raise RuntimeError(f"selftest checkpoint load failed: {why}")
        r2 = np.random.default_rng(0); r2.bit_generator.state = cp["rng_state"]
        tail = r2.normal(size=(n-cut, 4))
        # Compare against an independently generated continuation of the same RNG.
        r3 = np.random.default_rng(seed); _ = r3.normal(size=(cut,4)); tail_ref = r3.normal(size=(n-cut,4))
        if not np.array_equal(tail, tail_ref):
            raise RuntimeError("selftest RNG continuation mismatch")
        print("BM-A030_CHECKPOINT_SELFTEST_PASS", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package-root")
    ap.add_argument("--raw-dir")
    ap.add_argument("--r3-root")
    ap.add_argument("--out-dir")
    ap.add_argument("--recordings", nargs="*")
    ap.add_argument("--smoke-B", type=int, default=None)
    ap.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK)
    ap.add_argument("--checkpoint-selftest", action="store_true")
    ap.add_argument("--plan-only", action="store_true")
    args = ap.parse_args()
    if args.checkpoint_selftest:
        checkpoint_selftest(); return
    for x in ["package_root", "raw_dir", "r3_root", "out_dir"]:
        if not getattr(args, x):
            raise SystemExit(f"--{x.replace('_','-')} is required")
    if args.smoke_B is not None and not (1 <= args.smoke_B <= B_FROZEN):
        raise SystemExit("--smoke-B out of range")
    if not (1 <= args.chunk_size <= B_FROZEN):
        raise SystemExit("--chunk-size out of range")
    run(args)


if __name__ == "__main__":
    main()