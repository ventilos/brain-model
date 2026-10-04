# Brain Model — CHANGELOG

This file records substantive scientific, methodological, computational, provenance, and repository-governance changes in the Brain Model (BM-2026) project.

Historical operations predating this Git repository remain documented in their original provenance records and migration ledger. Their absence from this file must not be interpreted as absence of provenance.

Changes recorded here do not by themselves constitute scientific results or promote the status of an analysis.

## 2026-10-04 — BM-A031 pre-publication repository hardening

**Scope:** repository governance and pre-publication preparation only.  
**Scientific impact:** NONE. No G1 analysis was reopened and no full G2 execution was performed.

### Repository status transition

Repository phase advanced from:

`ACTIVE / CONTROLLED MIGRATION`

to:

`ACTIVE / PRE-PUBLICATION HARDENING`

The transition follows completion of the previously documented local
BM-A031 canonical source promotion, canonical regression-test path
synchronization, and local regression verification.

No scientific code, frozen protocol rule, Amendment-002 semantic rule,
estimator, threshold, or checkpoint contract was changed by this
status transition.

### Current repository gate

Previous gate:

`BM-A031_CANONICALIZATION_BUNDLE_COMMIT_AND_REMOTE_VERIFICATION`

Current gate:

`BM-A031_PREPUBLICATION_REPOSITORY_HARDENING`

Canonicalization bundle commit:

`COMPLETE`

Canonical commit:

`311d0e5`

Local repository verification:

`PASS`

Independent remote GitHub verification:

`DEFERRED / NOT INDEPENDENTLY VERIFIED`

Independent remote verification remains desirable but is not treated
as a prerequisite for pre-publication repository hardening.

If public release occurs before independent remote verification,
release documentation must explicitly retain:

`REMOTE_REPOSITORY_NOT_INDEPENDENTLY_VERIFIED`

The absence of independent remote verification is not classified as a
scientific or local repository-verification failure.

### Scientific lock

Scientific lock remains:

`BM-A011 R3 frozen / G1 closed`

Frozen G1 result remains:

`RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS`

G2 status remains:

`FULL_G2_NOT_RUN`

Scientific status remains:

`FULL_G2_NOT_RUN / G1_UNCHANGED`

No new scientific result or claim is introduced by this operation.

### Current phase

The project has entered controlled pre-publication repository hardening.

Current work concerns repository reproducibility, documentation,
environment specification, automated testing, provenance, release
integrity, and publication readiness.

Repository hardening and publication operations remain distinct from
scientific validation and from execution of the prespecified full G2
analysis.

### Change classification

`DOCUMENTATION / REPOSITORY GOVERNANCE / PRE-PUBLICATION HARDENING`

Scientific-impact classification:

`NONE`


## 2026-10-03 — BM-A031 Rev2 canonical source promotion

- Operation: controlled repository canonicalization.
- Source artifact:
  `archive/provenance/BM-A031_G2_PATCHED_RUNNER.py`
- Canonical promoted artifact:
  `src/BM-A031_G2_PATCHED_RUNNER.py`
- Promotion method: byte-identical copy; archival provenance artifact retained.
- Verified SHA-256:
  `f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`
- Integrity verification: PASS.
- Scientific code modification: NONE.
- Amendment-002 semantics: UNCHANGED.
- Scientific status: `FULL_G2_NOT_RUN / G1_UNCHANGED`.
- Audit state before promotion: `A PASS / B PASS / C PASS 7/7 / D PASS / E PASS`.
- Promotion status: `CANONICAL_SOURCE_COPIED_AND_HASH_VERIFIED`.
- The regression test remains pointed at the archived provenance runner; no test-path change is included in this operation.
### BM-A031 Rev2 — canonical regression-test path synchronization

- Operation: canonical regression-test path synchronization.
- Test:
  `tests/test_bm_a031_amendment002_rev2.py`
- Previous runner target:
  `archive/provenance/BM-A031_G2_PATCHED_RUNNER.py`
- Canonical runner target:
  `src/BM-A031_G2_PATCHED_RUNNER.py`
- Change scope:
  `PATH-ONLY / TEST LOGIC UNCHANGED`
- Previous verified test SHA-256:
  `c126618eaa22d2e1587efa3f6c469cf60e8c85563bbdf5f4e262f955cd9178ff`
- Current canonical-path test SHA-256:
  `1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2`
- Canonical runner SHA-256:
  `f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`
- Regression verification against canonical `src/` runner:
  `7 / 7 PASS`
- Amendment-002 semantics:
  `UNCHANGED`
- Scientific code modification:
  `NONE`
- Gate:
  `BM-A031_CANONICAL_TEST_PATH_SYNC = PASS`
- Scientific status:
  `FULL_G2_NOT_RUN / G1_UNCHANGED` 
## 2026-10-03 — BM-A031 Rev2 repository correction and pre-promotion audit

**Audit start:** 2026-10-03T16:25:00+02:00 (Europe/Warsaw) / 2026-10-03T14:25:00Z  
**Scope:** repository migration, structural correction, provenance verification, and pre-promotion audit only.  
**Scientific impact:** NONE. No new G2 result was generated.

### Repository corrections

- Corrected the canonical repository placement of the BM-A031 Rev2 runner and regression test.
- Canonical runner path:
  `archive/provenance/BM-A031_G2_PATCHED_RUNNER.py`
- Canonical regression-test path:
  `tests/test_bm_a031_amendment002_rev2.py`
- Corrected the migration-ledger filename:
  `docs/MIGRATION_LEDGER.md.` → `docs/MIGRATION_LEDGER.md`
- Verified after rename that the migration ledger retained the Amendment-002 content.
- Verified the corrected repository tree on `main`.

### Artifact integrity

BM-A031 Rev2 runner:

`SHA-256 f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`

BM-A031 Rev2 regression test:

`SHA-256 eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d`

Artifact identity verification: **PASS**.

### Pre-promotion audit

Five audit layers were evaluated:

- Audit A — artifact integrity and identity: **PASS**
- Audit B — Amendment-002 / frozen G2 computational semantics: **PASS**
- Audit C — Python compilation and Rev2 regression verification: **PASS (7/7)**
- Audit D — checkpoint V3 / provenance / fail-closed contract: **PASS**
- Audit E — scientific-status consistency: **PASS**

The audit confirmed preservation of:

- state order `LL, LH, HL, HH`;
- undefined zero-outgoing transition rows;
- finite-only null aggregation;
- original `q_obs` weighting without renormalization;
- Amendment-002 reporting requirements;
- N2 run-local transition boundaries;
- checkpoint schema V3;
- runner SHA-256 in the checkpoint contract;
- Amendment-002 identifier in the checkpoint contract;
- fail-closed handling of incompatible checkpoint contracts;
- explicit undefined-row reporting.

The existing methodological caveat for partially defined null-median rows in `D_M1` is retained unchanged. No post-freeze modification of the Amendment-002 computational rule was introduced.

### Scientific lock

BM-A011 R3 remains frozen.

G1 remains closed and unchanged.

Full BM-A031 Rev2 G2 has **NOT** been run.

No G2 scientific result is asserted by this repository correction or audit.

No mechanism, treatment, absence-of-memory, or generalized Brain Model claim is promoted.

### Current status

`PRE-PROMOTION_AUDIT_PASS / PROTOCOL_COMPATIBILITY_VERIFIED / CORE_MATH_VERIFIED / AMENDMENT002_REPORTING_COMPLIANT / CHECKPOINT_V3_CONTRACT_VERIFIED / FULL_G2_NOT_RUN / G1_UNCHANGED / NOT_YET_PROMOTED`

Promotion to the canonical source tree remains a separate controlled operation.

## 2026-10-03 — BM-A031 Rev2 regression-test path correction

**Scope:** repository-path correction and provenance clarification only.  
**Scientific impact:** NONE. No G2 scientific computation was performed and no frozen Amendment-002 rule was changed.

### Correction

The BM-A031 Rev2 regression test was corrected to reference the runner at its actual canonical repository location:

`archive/provenance/BM-A031_G2_PATCHED_RUNNER.py`

The previous test path contained an erroneous intermediate `BM-A031/` directory:

`archive/provenance/BM-A031/BM-A031_G2_PATCHED_RUNNER.py`

Only the `RUNNER` path declaration in:

`tests/test_bm_a031_amendment002_rev2.py`

was changed.

### Integrity verification

The corrected regression test contains 110 lines and the same 7 regression tests as the previously verified version.

Corrected regression-test SHA-256:

`c126618eaa22d2e1587efa3f6c469cf60e8c85563bbdf5f4e262f955cd9178ff`

The previous file can be reconstructed exactly by restoring only the removed intermediate path component `/ „BM-A031”`, yielding the previous verified SHA-256:

`eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d`

Therefore the correction is classified as:

`PATH-ONLY CHANGE / TEST LOGIC UNCHANGED / AMENDMENT-002 SEMANTICS UNCHANGED`

The BM-A031 runner itself was not modified. Its verified SHA-256 remains:

`f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`

### Scientific lock

Full BM-A031 Rev2 G2 remains **NOT RUN**.

G1 remains unchanged.

No scientific claim is promoted by this correction.