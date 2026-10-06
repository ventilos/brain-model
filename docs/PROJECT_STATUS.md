# Brain Model — Project Status

**Project:** Brain Model (BM-2026)  
**Repository:** brain-model  
**Canonical branch:** main  
**Status:** ACTIVE / PRE-PUBLICATION HARDENING  
**Scientific lock:** BM-A011 R3 frozen / G1 closed  
**G2 status:** FULL_G2_NOT_RUN  
**Last updated:** 2026-10-06

## Purpose

This file is the canonical entry point for the current state of the Brain Model project.

It distinguishes the current scientific state from historical analyses, superseded implementations, audit artifacts, generated results, provenance records, and external/raw data.

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

G0 (BM-A028 decision): `PASS` — strict 38/38 checkpoint validation, all AUDIT_12X production audits PASS, final group summary consistent with the run contract.

G1 result:

`RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS`

Empirical group p-values: `common_phase_run` 0.8773, `epochwise_common_phase` 0.1264 (primary); `independent_channel_phase` 0.1152 (sensitivity only).

This result remains locked.

The repository migration, audit, Amendment-002 implementation verification, BM-A031 canonicalization and publication-readiness work do not reopen G1.

Current G2 status:

`FULL_G2_NOT_RUN`

The only G2 outputs recorded in the project library come from an exact-replay smoke test (BM-A029, B = 2, recording ST7011, status `SMOKE_ONLY`, 2026-10-02, before Amendment-002), which computes no population diagnostics.

## Operative BM-A027 protocol lineage

The operative G2 protocol lineage consists of:

- `BM-A027_PREREGISTRATION.md` (BM-A027 / BM-CHALLENGE-001 v1.0)
- `BM-A027_AMENDMENT_001_PREOUTCOME_SOURCE_CONSISTENCY_2026-09-29.md`
- `BM-A027_AMENDMENT_002_G2_UNDEFINED_TRANSITION_ROWS.md`
- `BM-A027_CHALLENGE001_FROZEN_CONFIG.json`

Since 2026-10-06 the repository copies of v1.0 and Amendment-001 are byte-identical to the frozen library files (SHA-256 in `docs/MIGRATION_LEDGER.md`, section 16). The frozen configuration is a v1.0 artifact: where its G3/G4 entries differ from Amendment-001 (G3 model families; G4 separated from the primary chain), Amendment-001 controls.

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

Canonical source runner:

`src/BM-A031_G2_PATCHED_RUNNER.py`

Archived provenance runner (byte-identical):

`archive/provenance/BM-A031_G2_PATCHED_RUNNER.py`

Verified runner SHA-256:

`f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`

The canonical source was created on 2026-10-03 (commit `311d0e5`) as a byte-identical copy of the verified archived provenance runner.

Promotion integrity:

`BYTE-IDENTICAL / PASS`

Scientific code modification during promotion:

`NONE`

Amendment-002 semantics:

`UNCHANGED`

## Regression verification

Regression test:

`tests/test_bm_a031_amendment002_rev2.py` — targets the canonical runner `src/BM-A031_G2_PATCHED_RUNNER.py`

Current regression-test SHA-256:

`1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2`

Regression verification against the canonical `src/` runner:

`7 / 7 PASS`

Historical regression-test identities (path-only changes; test logic unchanged):

| SHA-256 | Runner path targeted | Period |
|—|—|—|
| `eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d` | `archive/provenance/BM-A031/…` (erroneous intermediate directory) | until 2026-10-03 |
| `c126618eaa22d2e1587efa3f6c469cf60e8c85563bbdf5f4e262f955cd9178ff` | `archive/provenance/BM-A031_G2_PATCHED_RUNNER.py` | 2026-10-03 |
| `1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2` | `src/BM-A031_G2_PATCHED_RUNNER.py` | current |

Test logic:

`UNCHANGED`

Amendment-002 semantics:

`UNCHANGED`

## CI contract — BM-CI-CERT-001 v0.2

- Verifier: `tools/verify_ci_contract.py`; workflow: `.github/workflows/ci-cert.yml`; environment: `requirements-ci.txt`.
- Frozen controls: Python 3.13.5; numpy 2.3.5; pandas 2.2.3; scipy 1.17.0; pytest 9.0.2; SHA-256 of the runner, the regression test, `requirements-ci.txt` and `ci-cert.yml`.
- Local CI contract: `PASS` (2026-10-05).
- Remote GitHub Actions status: `NOT YET VERIFIED` — record the run URL here once both workflows are green on main.
- Boundary: `CI_CONTRACT_PASS` is not `FULL_PROJECT_REPRODUCIBILITY_PASS`; full-project reproducibility remains `NOT_TESTED`.
- Delivery record: `docs/provenance/ci/BM-CI-CERT-001_v0.2/`.
- Post-push CI verification (2026-10-06):
- HEAD: `eeb5f36`
- BM CI Contract — BM-A031 Rev2 #18: PASS
- Run: https://github.com/ventilos/brain-model/actions/runs/37472826228

## Checkpoint contract

BM-A031 Rev2 uses:

`CHECKPOINT_SCHEMA = 3`

Execution identity:

`BM-A031-G2-SMART-RESUME-CHECKPOINT-V3`

Applicable G2 amendment:

`BM-A027-AMENDMENT-002`

The verified implementation uses a fail-closed checkpoint contract and records the relevant analysis identity, runner identity, state order, undefined-row policy, and source/reference hashes.

Checkpoint incompatibility does not silently resume an incompatible run.

## Pre-canonicalization audit

The controlled audit completed before canonical source promotion has the following status:

- Audit A — PASS
- Audit B — PASS
- Audit C — PASS, 7/7 regression tests
- Audit D — PASS
- Audit E — PASS

This audit establishes implementation/provenance consistency for the verified BM-A031 Rev2 artifact.

It does **not** constitute execution of full G2.

## Current repository state

The controlled repository contains:

- repository governance/documentation (`README.md`, `CHANGELOG.md`, this file, `docs/MIGRATION_LEDGER.md`);
- licensing and citation files (`LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, `docs/LICENSE-DOCS.md`, `CITATION.cff`);
- BM-A027 protocol and amendments, and the frozen BM-A027 configuration;
- the BM-A031 Rev2 compatibility/provenance record;
- the canonical BM-A031 Rev2 runner under `src/` and its archived provenance copy;
- the BM-A031 regression test;
- the BM-CI-CERT-001 v0.2 CI contract and its delivery record.

Not yet migrated: the BM-A011 R3 scientific package, the R3 outputs and the BM-A028 G0/G1 decision record (see `docs/MIGRATION_LEDGER.md`).

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

`BM-A031_PREPUBLICATION_REPOSITORY_HARDENING`

Previous gate: `BM-A031_CANONICALIZATION_BUNDLE_COMMIT_AND_REMOTE_VERIFICATION` — canonicalization bundle committed (`311d0e5`); independent remote verification deferred (CHANGELOG, 2026-10-04).

Open items before an archival (DOI) release:

1. Migrate or deposit the frozen BM-A011 R3 scientific package (SHA-256 `9ab675e3acd157b21845f5f242b43274337c6cb4f5121efc59ad03a84110414f`), the R3 result archive (SHA-256 `20b6e95d482c3371ce5b95ee44f861b6f39f327dbbd61d40fe276e674c6726f3`) and the BM-A028 G0/G1 decision record.
2. Execute and record full G2.
3. Remote verification: both GitHub Actions workflows green on the release commit; otherwise the release notes state `REMOTE_REPOSITORY_NOT_INDEPENDENTLY_VERIFIED`.
4. Add the DOI of the new preprint (in preparation) to `README.md` and `CITATION.cff`.

Operational rule for production G2: run on the complete locked inventory only. BM-A031 Rev2 labels every run without `—smoke-B` as `G2_COMPLETE`, including a run restricted with `—recordings` (observed in a synthetic end-to-end harness on 2026-10-06). A subset run must never be reported as full G2.

No full G2 execution is authorized merely by completion of repository hardening.

Scientific status remains:

`FULL_G2_NOT_RUN / G1_UNCHANGED`

## Current phase

Pre-publication hardening of the canonical Brain Model repository.

Canonical source promotion and local canonicalization are complete.

Current work concerns repository reproducibility, documentation, environment specification, automated testing, provenance, release integrity, and publication readiness.

Repository engineering and publication operations remain distinct from scientific validation and from execution of the prespecified full G2 analysis.

Independent remote repository verification remains deferred and does not modify the frozen scientific state.

## Publication

A new preprint is in preparation (decision of 2026-10-06). Preprint v1.0 of 2026-10-02 is retained as historical provenance and is not the publication reference for this repository.
