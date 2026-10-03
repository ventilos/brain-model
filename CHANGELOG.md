# Brain Model — CHANGELOG

This file records substantive scientific, methodological, computational, provenance, and repository-governance changes in the Brain Model (BM-2026) project.

Historical operations predating this Git repository remain documented in their original provenance records and migration ledger. Their absence from this file must not be interpreted as absence of provenance.

Changes recorded here do not by themselves constitute scientific results or promote the status of an analysis.


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