#!/usr/bin/env python3
"""BM-CI-CERT-001 v0.2 — fail-closed checks for the frozen BM-A031 Rev2 contract.

Scope is deliberately narrow. PASS does NOT mean full-project reproducibility or FULL_G2.
"""
from __future__ import annotations
import hashlib
import importlib.metadata as md
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "src" / "BM-A031_G2_PATCHED_RUNNER.py"
ARCHIVE_RUNNER = ROOT / "archive" / "provenance" / "BM-A031_G2_PATCHED_RUNNER.py"
TEST = ROOT / "tests" / "test_bm_a031_amendment002_rev2.py"
STATUS = ROOT / "docs" / "PROJECT_STATUS.md"
REQ = ROOT / "requirements-ci.txt"
WORKFLOW = ROOT / ".github" / "workflows" / "ci-cert.yml"

EXPECTED_HASHES = {
    RUNNER: "f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b",
    TEST: "1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2",
    REQ: "2905ba50505ca0a4dd03ae415e4e8e84dedb4d4ef560fa8e051e4306aa681553",
    WORKFLOW: "a6c8644c417419fcfba2a5d155f992f5944fbebcf087e59db224a2b9dc80c968",
}
EXPECTED_VERSIONS = {
    "numpy": "2.3.5",
    "pandas": "2.2.3",
    "scipy": "1.17.0",
    "pytest": "9.0.2",
}
EXPECTED_PYTHON = (3, 13, 5)

class ContractFailure(RuntimeError):
    pass

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def verify_one_hash(path: Path, expected: str) -> None:
    if not path.is_file():
        raise ContractFailure(f"missing required file: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    got = sha256(path)
    if got != expected:
        raise ContractFailure(f"sha256 mismatch for {path.name}: {got} != {expected}")

def verify_hashes() -> None:
    for path, expected in EXPECTED_HASHES.items():
        verify_one_hash(path, expected)
        print(f"PASS sha256 {path.relative_to(ROOT)} {expected}")

def verify_promotion_identity() -> None:
    if not ARCHIVE_RUNNER.is_file():
        raise ContractFailure("archived provenance runner missing")
    if RUNNER.read_bytes() != ARCHIVE_RUNNER.read_bytes():
        raise ContractFailure("canonical runner differs from archived provenance runner")
    print("PASS canonical/archive runner byte-identical")

def verify_scientific_guardrail() -> None:
    if not STATUS.is_file():
        raise ContractFailure("PROJECT_STATUS.md missing")
    text = STATUS.read_text(encoding="utf-8")
    required = ["FULL_G2_NOT_RUN", "G1_UNCHANGED", "REGRESSION_7_OF_7_PASS"]
    missing = [x for x in required if x not in text]
    if missing:
        raise ContractFailure(f"PROJECT_STATUS missing guardrails: {missing}")
    print("PASS scientific-status guardrails present")

def verify_environment() -> None:
    got_py = sys.version_info[:3]
    if got_py != EXPECTED_PYTHON:
        raise ContractFailure(f"Python version {got_py} != {EXPECTED_PYTHON}")
    print("PASS Python==3.13.5")
    for package, expected in EXPECTED_VERSIONS.items():
        got = md.version(package)
        if got != expected:
            raise ContractFailure(f"version {package}: {got} != {expected}")
        print(f"PASS version {package}=={got}")

def negative_integrity_selftest() -> None:
    # Exercise the SAME verifier used by the real contract and require rejection.
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / RUNNER.name
        shutil.copy2(RUNNER, p)
        with p.open("ab") as f:
            f.write(b"\n# BM-CI-CERT-001-v0.2 deliberate mutation\n")
        try:
            verify_one_hash(p, EXPECTED_HASHES[RUNNER])
        except ContractFailure:
            print("PASS negative integrity self-test: mutated artifact rejected")
        else:
            raise ContractFailure("negative integrity self-test: mutated artifact was accepted")

def main() -> int:
    try:
        verify_hashes()
        verify_promotion_identity()
        verify_scientific_guardrail()
        verify_environment()
        negative_integrity_selftest()
    except (ContractFailure, FileNotFoundError, md.PackageNotFoundError) as exc:
        print(f"BM-CI-CERT-001 v0.2 CONTRACT FAIL: {exc}", file=sys.stderr)
        return 1
    print("BM-CI-CERT-001 v0.2 CI_CONTRACT_PASS")
    print("FULL_PROJECT_REPRODUCIBILITY=NOT_TESTED")
    print("FULL_G2=NOT_RUN")
    print("G1=UNCHANGED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
