# Brain Model — Project Status

**Project:** Brain Model (BM-2026)  
**Repository:** brain-model  
**Canonical branch:** main  
**Status:** ACTIVE / CONTROLLED MIGRATION  
**Scientific lock:** BM-A011 R3 frozen / G1 closed  
**G2 status:** FULL_G2_NOT_RUN

## Purpose

This file is the canonical entry point for the current state of the Brain Model project.

It distinguishes the current scientific state from historical analyses,
superseded implementations, audit artifacts, generated results,
provenance records, and external/raw data.

## Repository principles

1. The repository must remain reproducible and auditable.
2. Current source code must be separated from historical and superseded artifacts.
3. Raw datasets must not be committed unless explicitly approved.
4. Generated results must remain distinguishable from source inputs.
5. Scientific claims must remain traceable to their source analysis and implementation.
6. Historical artifacts are retained for provenance but do not automatically define the current implementation.
7. Changes to the canonical implementation must be recorded in CHANGELOG.md and Git history.
8. Repository restructuring must not silently alter scientific status.
9. Negative results and frozen decisions must be retained.
10. Full G2 must not be represented as executed until the complete prespecified run has actually been performed.

## Current scientific lock

The current frozen scientific state remains:

`BM-A011 R3`

G1 result:

`RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS`

This result remains locked.

The present repository migration, audit, Amendment-002 implementation
verification, and BM-A031 canonicalization do not reopen G1.

Current G2 status:

`FULL_G2_NOT_RUN`

## Operative BM-A027 protocol lineage

The operative G2 protocol lineage consists of:

- `BM-A027_PREREGISTRATION.md`
- `BM-A027_AMENDMENT_001_PREOUTCOME_SOURCE_CONSISTENCY_2026-09-29.md`
- `BM-A027_AMENDMENT_002_G2_UNDEFINED_TRANSITION_ROWS.md`
- `BM-A027_CHALLENGE001_FROZEN_CONFIG.json`

Amendment-002 freezes, among other implementation details:

- state order: `LL, LH, HL, HH`;
- zero-outgoing transition rows as undefined/NaN rather than zero vectors;
- finite-only null aggregation for affected transition quantities;
- original `q_obs` weights without renormalization for the frozen finite-pair rule;
- run-local N2 transition boundaries;
- explicit undefined-row reporting;
- checkpoint identity/provenance requirements.

These rules do not alter the frozen G1 result.

## BM-A031 Rev2 — verified implementation state

Archived provenance runner:

`archive/provenance/BM-A031_G2_PATCHED_RUNNER.py`

Canonical source runner:

`src/BM-A031_G2_PATCHED_RUNNER.py`

Verified runner SHA-256:

`f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`

The canonical source was created as a byte-identical copy of the verified
archived provenance runner.

Promotion integrity:

`BYTE-IDENTICAL / PASS`

Scientific code modification during promotion:

`NONE`

Amendment-002 semantics:

`UNCHANGED`

## Regression verification

Regression test:

`tests/test_bm_a031_amendment002_rev2.py`

Current verified test SHA-256:

`c126618eaa22d2e1587efa3f6c469cf60e8c85563bbdf5f4e262f955cd9178ff`

Historical pre-path-correction test SHA-256:

`eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d`

The change between those test artifacts was a repository-path-only
correction.

Independent repository-equivalent regression execution:

`7 / 7 PASS`

The regression test now targets the canonical runner:

`src/BM-A031_G2_PATCHED_RUNNER.py`

Canonical test-path synchronization:

`PASS`

Current canonical-path regression-test SHA-256:

`1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2`

Regression verification against the canonical `src/` runner:

`7 / 7 PASS`

The test-path synchronization was a path-only change.

Test logic:

`UNCHANGED`

Amendment-002 semantics:

`UNCHANGED`

## Checkpoint contract

BM-A031 Rev2 uses:

`CHECKPOINT_SCHEMA = 3`

Execution identity:

`BM-A031-G2-SMART-RESUME-CHECKPOINT-V3`

Applicable G2 amendment:

`BM-A027-AMENDMENT-002`

The verified implementation uses a fail-closed checkpoint contract and
records the relevant analysis identity, runner identity, state order,
undefined-row policy, and source/reference hashes.

Checkpoint incompatibility does not silently resume an incompatible run.

## Pre-canonicalization audit

The controlled audit completed before canonical source promotion has the
following status:

- Audit A — PASS
- Audit B — PASS
- Audit C — PASS, 7/7 regression tests
- Audit D — PASS
- Audit E — PASS

This audit establishes implementation/provenance consistency for the
verified BM-A031 Rev2 artifact.

It does **not** constitute execution of full G2.

## Current repository state

The controlled repository now contains, at minimum:

- repository governance/documentation;
- BM-A027 protocol and amendments;
- frozen BM-A027 configuration;
- BM-A031 provenance runner;
- BM-A031 compatibility/provenance record;
- BM-A031 regression test;
- canonical BM-A031 Rev2 runner under `src/`.

The archival runner is intentionally retained after canonical promotion.

## Current implementation status

`PROTOCOL_COMPATIBILITY_VERIFIED`

`CORE_MATH_VERIFIED`

`AMENDMENT002_REPORTING_COMPLIANT`

`CHECKPOINT_V3_CONTRACT_VERIFIED`

`REGRESSION_7_OF_7_PASS`

`CANONICAL_SOURCE_HASH_VERIFIED`

`FULL_G2_NOT_RUN`

`G1_UNCHANGED`

## Current gate

`BM-A031_CANONICALIZATION_BUNDLE_COMMIT_AND_REMOTE_VERIFICATION`

Canonical source promotion and canonical regression-test path
synchronization have been completed locally and independently verified.

Canonical-path regression verification:

`7 / 7 PASS`

Current canonical-path regression-test SHA-256:

`1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2`

Canonical runner SHA-256:

`f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`

The next controlled operation is commit and remote verification of the
canonicalization bundle.

No full G2 execution is authorized merely by completion of repository
canonicalization.

Scientific status remains:

`FULL_G2_NOT_RUN / G1_UNCHANGED`

## Current phase

Controlled migration and canonicalization of the latest verified Brain
Model implementation.

Repository engineering operations remain distinct from scientific
validation and from execution of the prespecified full G2 analysis.