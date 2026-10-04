Brain Model — Migration Ledger

Project: Brain Model (BM-2026)
Repository: brain-model
Canonical branch: main
Migration status: IN PROGRESS
Purpose: controlled migration of Brain Model artifacts into the canonical Git repository.

1. Migration rule

No historical package or analysis directory is copied wholesale into the canonical source tree.

Every artifact must be classified before migration as one of:

• CURRENT — current canonical project state or active analysis
• SOURCE — executable scientific source code
• TEST — validation, regression, smoke, or integrity test
• CONFIG — frozen configuration or preregistration contract
• GENERATED — reproducible output generated from source/configuration
• PROVENANCE — audit, execution, lineage, checksum, or historical record
• SUPERSEDED — retained only for history/reproducibility
• EXTERNAL/RAW — external or raw data; referenced but not committed unless explicitly approved

2. Current ST44 and post-lock implementation/diagnostic lineage

Current verified lineage:

BM-A011 R3
→ BM-A027 preregistration / BM-CHALLENGE-001
→ Amendment-001
→ BM-A028 G0/G1 decision
→ BM-A029 G2 implementation
→ BM-A030 resumable G2 runner
→ BM-A031 candidate corrective G2 patch
→ BM-A027 Amendment-002 (pre-execution undefined-transition-row rule)
→ BM-A031 Rev2 Amendment-002-compatible implementation
→ BM-A032 positive-control / injection-recovery diagnostic

The locked BM-A011 R3 and G1 result must not be silently modified by later analyses.

BM-A031 and BM-A032 are post-lock implementation/diagnostic developments. Their existence does not alter the frozen BM-A011 R3 result or reopen G1.

3. Artifact ledger

|Artifact                                       |Classification         |Status                                                                                                                                     |Target / policy                                                                                    |
|————————————————|————————|-——————————————————————————————————————————————|—————————————————————————————————|
|README.md                                      |CURRENT                |MIGRATED                                                                                                                                   |repository root                                                                                    |
|CHANGELOG.md                                   |CURRENT / PROVENANCE   |MIGRATED                                                                                                                                   |repository root                                                                                    |
|.gitignore                                     |CONFIG                 |MIGRATED                                                                                                                                   |repository root                                                                                    |
|docs/PROJECT_STATUS.md                         |CURRENT                |MIGRATED                                                                                                                                   |docs/                                                                                              |
|docs/MIGRATION_LEDGER.md                       |CURRENT / PROVENANCE   |CURRENT — UPDATE PREPARED                                                                                                                  |docs/                                                                                              |
|BM-A011 R3 scientific package                  |SOURCE / PROVENANCE    |FROZEN                                                                                                                                     |classify contents before migration                                                                 |
|BM-A011 R3 outputs                             |GENERATED              |FROZEN                                                                                                                                     |results/ after manifest verification                                                               |
|BM-A027 preregistration                        |CONFIG / PROVENANCE    |FROZEN / MIGRATED                                                                                                                          |docs/provenance/                                                                                   |
|BM-A027 Amendment-001                          |CONFIG / PROVENANCE    |FROZEN / MIGRATED                                                                                                                          |docs/provenance/                                                                                   |
|BM-A027 Amendment-002                          |CONFIG / PROVENANCE    |FROZEN / MIGRATED                                                                                                                          |docs/provenance/; pre-execution G2 undefined-transition-row policy                                 |
|BM-A027 frozen config                          |CONFIG / PROVENANCE    |FROZEN / MIGRATED / BYTE-INTEGRITY VERIFIED                                                                                                |docs/provenance/; expected SHA-256 b15436dca3970fb680dde7b71bd03e7ebef1c309de351907a1645ee5b4fa04b3|
|BM-A028 G0/G1 decision                         |PROVENANCE / GENERATED |FROZEN                                                                                                                                     |docs/provenance/ or results/                                                                       |
|BM-A029 G2 replay                              |SOURCE                 |SUPERSEDED FOR EXECUTION                                                                                                                   |archive/provenance after verification                                                              |
|BM-A030 resumable runner                       |SOURCE / PROVENANCE    |SUPERSEDED FOR EXECUTION                                                                                                                   |archive/provenance after verification                                                              |
|BM-A031 original patched G2 runner             |SOURCE / PROVENANCE    |SUPERSEDED BY BM-A031 REV2                                                                                                                 |preserve in provenance/history; do not use for full G2                                             |
|BM-A031 Rev2 patched G2 runner                 |SOURCE / PROVENANCE    |PROTOCOL_COMPATIBILITY_VERIFIED / CORE_MATH_VERIFIED / AMENDMENT002_REPORTING_COMPLIANT / CHECKPOINT_V3_CONTRACT_VERIFIED / FULL_G2_NOT_RUN|archived verified candidate; not yet canonical src/                                                |
|BM-A031 Rev2 regression test                   |TEST                   |PREPARED / REGRESSION PASS IN CONTROLLED TEST STRUCTURE                                                                                    |tests/; reposit                                                         |
|BM-A031 original patch note                    |PROVENANCE             |HISTORICAL                                                                                                                                 |retain unchanged; refers to earlier runner identity                                                |
|BM-A031 Rev2 Amendment-002 compatibility record|PROVENANCE             |CURRENT                                                                                                                                    |Library + provenance migration target                                                              |
|BM-A032 frozen protocol                        |CONFIG / PROVENANCE    |CURRENT DIAGNOSTIC                                                                                                                         |configs/ + docs/provenance/ after verification                                                     |
|BM-A032 Phase-A runner                         |SOURCE / TEST          |CURRENT DIAGNOSTIC                                                                                                                         |tests/ or scripts/ after verification                                                              |
|BM-A032 Phase-A outputs                        |GENERATED              |REVIEW                                                                                                                                     |results/diagnostics/                                                                               |
|BM-A032 execution record                       |PROVENANCE             |CURRENT                                                                                                                                    |docs/provenance/                                                                                   |
|BM ST44 R3 preprint v1.0                       |PROVENANCE / DOCUMENT  |CURRENT PUBLICATION DRAFT                                                                                                                  |docs/preprint/                                                                                     |
|BM-PKG-001                                     |SUPERSEDED / PROVENANCE|SUPERSEDED                                                                                                                                 |archive only                                                                                       |
|BM-PKG-002                                     |PROVENANCE             |HISTORICAL REPRODUCIBILITY BASELINE                                                                                                        |archive/provenance; not canonical source                                                           |
|Sleep-EDF / ST44 raw EDF data                  |EXTERNAL/RAW           |EXTERNAL                                                                                                                                   |DO NOT COMMIT                                                                                      |
|External HDF5/raw datasets                     |EXTERNAL/RAW           |EXTERNAL                                                                                                                                   |DO NOT COMMIT                                                                                      |

4. Scientific lock

The following BM-A011 R3 properties remain frozen during migration:

• cohort: 19 participants / 38 recordings
• surrogate count: B = 1999 per recording × variant
• master seed: 20260921
• support: contiguous N2 runs
• transitions never cross N2-run boundaries
• statistic: T_cs on common target support
• primary nulls:
  • common_phase_run
  • epochwise_common_phase
• sensitivity null:
  • independent_channel_phase

G1 is closed.

Later code migration, G2 diagnostics, positive controls, repository restructuring, documentation changes, or implementation corrections must not retroactively alter the locked G1 result.

5. Current G1 state

Locked status:

RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS

This is a bounded statistical result.

It must not be promoted to claims that:

• neural memory is absent;
• temporal dependence is absent;
• nonlinear dynamics are absent;
• every Brain Model representation is falsified;
• preserved spectra or phase structure explain all relevant neural dynamics.

The result applies to the frozen ST44 operator, statistic, cohort, support definition and prespecified common-phase null hierarchy.

6. BM-A027 operative preregistration state

The operative BM-A027 preregistration consists of:

1. BM-A027 / BM-CHALLENGE-001 v1.0;
2. BM-A027 Amendment-001;
3. BM-A027 Amendment-002 for the pre-execution G2 undefined-transition-row implementation rule;
4. BM-A027 frozen machine-readable configuration.

Where Amendment-001 conflicts with the original v1.0 document, Amendment-001 controls for the scope it amends. Amendment-002 controls the subsequently frozen G2 undefined-transition-row implementation rule for its stated scope.

The operative primary chain remains:

G0 — execution integrity
→ G1 — inherited frozen R3 raw-signal null gate
→ G2 — mandatory lower-order diagnostic context
→ G3 — continuous-domain temporal value-added gate

External replication remains necessary for cross-dataset or general claims.

The representation/spectral multiverse originally described as G4 is not part of the primary G0–G3 ST44 chain after Amendment-001.

G2 defines:

• D_occ
• D_self
• D_M1
• z_T
• participant-cluster bootstrap B = 10000
• seed = 20260929

Amendment-002 additionally freezes, before full G2 execution:

• state order: LL, LH, HL, HH;
• zero-outgoing transition rows as undefined rather than artificial zero distributions;
• NaN/null representation of undefined rows;
• finite-only null aggregation for defined values;
• no artificial discrepancy contribution from wholly undefined observed rows in D_self/D_M1;
• no renormalization of q_obs after excluding undefined comparisons;
• checkpoint provenance including schema, runner SHA-256, state order, undefined-row policy and applicable amendment identifier;
• explicit reporting of undefined-row occurrence and null availability.

Amendment-002 does not reopen G1 and does not convert G2 into a new confirmatory hypothesis test.

7. BM-A031 state

BM-A031 is a post-preregistration corrective implementation of the G2 analysis layer. It does not reopen or modify G1.

The original BM-A031 patch is retained as historical provenance and has been superseded for prospective execution by BM-A031 Rev2.

Current BM-A031 Rev2 state:

PROTOCOL_COMPATIBILITY_VERIFIED
CORE_MATH_VERIFIED
AMENDMENT002_REPORTING_COMPLIANT
CHECKPOINT_V3_CONTRACT_VERIFIED
FULL_G2_NOT_RUN
G1_UNCHANGED

BM-A031 Rev2 includes:

• state order: LL, LH, HL, HH;
• explicit undefined handling for transition rows with no observed outgoing transitions;
• finite-only null aggregation;
• Amendment-002-compatible D_self and D_M1 handling without artificial zero-distribution mismatch;
• checkpoint schema V3;
• runner SHA-256 in checkpoint contract;
• state-order, undefined-row-policy and Amendment-002 provenance in the contract;
• fail-closed behavior for incompatible checkpoint contracts;
• explicit reporting of observed undefined-row counts/frequencies, null availability and affected recording × variant cases;
• repository-relative regression-test targeting of the archived runner.

Verified BM-A031 Rev2 runner SHA-256:

f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b

Verified Rev2 regression-test SHA-256:

eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d

The original BM-A031 provenance note must not be silently rewritten to imply that it described Rev2. A separate Rev2 Amendment-002 compatibility record preserves the revision lineage.

BM-A031 Rev2 has not yet been promoted to canonical src/, and full G2 has not been executed.

8. BM-A032 state

BM-A032 is a diagnostic positive-control / injection-recovery analysis.

Current state:

REVIEW
SEQUENCE_LEVEL_DIAGNOSTIC_COMPLETE
RAW_SIGNAL_PHASE_B_NOT_RUN

Phase-A diagnostic:

• lambda = 0 rejection/recovery: 0.048
• lambda = 1 recovery: 0.000
• monotone adjacent pairs: 7/8

The first injection construction therefore did not validate as a suitable positive-control family.

BM-A032 Phase A must not be described as an empirical Sleep-EDF power estimate.

The next scientific step is diagnosis/revision of the positive-control generator before using it to make power claims.

BM-A032 does not alter the locked G1 result.

9. Historical packages

BM-PKG-001 is superseded.

BM-PKG-002 is retained as a historical reproducibility baseline.

BM-PKG-002 must not be treated as the current scientific state of Brain Model and must not be unpacked wholesale into the canonical source tree.

Historical packages may be retained under archive/provenance or referenced by checksum.

Historical reproducibility artifacts and current canonical implementation must remain distinguishable.

10. Raw-data policy

Raw or externally distributed datasets are not committed to Git.

The repository should contain instead, where appropriate:

• dataset identifiers
• acquisition instructions
• expected filenames
• checksums where legally and technically appropriate
• preprocessing contracts
• provenance records

No raw EDF/HDF5 dataset is migrated merely because it was used by a historical Brain Model analysis.

11. Migration verification

Before an artifact becomes canonical in Git, verify:

1. exact source identity;
2. version / analysis ID;
3. SHA-256 where available;
4. scientific status;
5. supersession relationship;
6. required dependencies;
7. expected target path;
8. reproducibility role;
9. whether it contains generated or external data;
10. whether migration changes scientific meaning;
11. whether implementation choices are covered by the applicable frozen protocol;
12. whether a post-preregistration methodological choice requires a separately frozen amendment;
13. whether tests operate from repository-relative paths on a clean checkout;
14. whether reporting requirements of the applicable amendment are explicitly implemented.

12. Planned canonical structure

The intended structure is:

brain-model/
├── README.md
├── CHANGELOG.md
├── .gitignore
├── docs/
│   ├── PROJECT_STATUS.md
│   ├── MIGRATION_LEDGER.md
│   ├── provenance/
│   └── preprint/
├── src/
├── tests/
├── scripts/
├── configs/
├── results/
│   └── diagnostics/
└── archive/

Directories are created only when the first classified artifact is ready for them.

Empty directory structure is not treated as a migration result because Git does not track empty directories.

13. Current migration gate

Current repository phase:

CONTROLLED MIGRATION

Completed migration gates:

• REPOSITORY_BOOTSTRAP
• PROJECT_STATUS_COMMITTED
• MIGRATION_LEDGER_CREATED
• BM-A027_PREREGISTRATION_BUNDLE_MIGRATED
• BM-A027_AMENDMENT002_FROZEN_AND_MIGRATED
• BM-A027_FROZEN_CONFIG_BYTE_INTEGRITY_VERIFIED
• BM-A031_REV2_PROTOCOL_COMPATIBILITY_VERIFIED
• BM-A031_REV2_AMENDMENT002_REPORTING_VERIFIED
• BM-A031_REV2_CHECKPOINT_V3_CONTRACT_VERIFIED

Previous gate:

BM-A031_PROTOCOL_COMPATIBILITY_PENDING — RESOLVED BY AMENDMENT-002 + BM-A031 REV2

Current canonicalization gate:

BM-A031_REV2_PRE_CANONICALIZATION_PROVENANCE_AND_CLEAN_CHECKOUT_VERIFICATION

Before promotion into canonical src/, retain the Rev2 provenance record, ensure the regression test is present in the repository, and verify the committed pair from a clean checkout or equivalent repository-isolated environment.

Full G2 must remain unexecuted until the intended executable identity and its applicable protocol/provenance are unambiguous.

14. Migration integrity note

Migration into Git is an archival and software-governance operation.

A Git commit does not by itself:

• validate a scientific result;
• promote a candidate implementation to canonical scientific status;
• convert an exploratory analysis into a preregistered analysis;
• reopen a closed inferential gate;
• change the interpretation of BM-A011 R3.

Scientific status is determined by the applicable frozen protocol, validated execution record and documented analysis lineage.

15. Current status summary

Repository:

ACTIVE / CONTROLLED MIGRATION

BM-A011 R3:

FROZEN / G1 CLOSED

BM-A027:

FROZEN PREREGISTRATION + AMENDMENT-001 + AMENDMENT-002 / MIGRATED / FROZEN CONFIG BYTE-INTEGRITY VERIFIED

BM-A031 Rev2:

PROTOCOL_COMPATIBILITY_VERIFIED / CORE_MATH_VERIFIED / AMENDMENT002_REPORTING_COMPLIANT / CHECKPOINT_V3_CONTRACT_VERIFIED / FULL_G2_NOT_RUN / G1_UNCHANGED

BM-A032:

REVIEW / SEQUENCE_LEVEL_DIAGNOSTIC_COMPLETE / RAW_SIGNAL_PHASE_B_NOT_RUN

Next canonicalization decision:

VERIFY THE COMMITTED BM-A031 REV2 RUNNER + REGRESSION TEST IN A CLEAN REPOSITORY CONTEXT, PRESERVE REV2 PROVENANCE, THEN DECIDE WHETHER TO PROMOTE THE EXACT VERIFIED RUNNER INTO CANONICAL src/.

## 2026-10-04 — Pre-publication licensing package

### Operation

`BM-2026_PREPUBLICATION_LICENSING_PACKAGE`

### Scope

Repository licensing and publication-governance update performed during
the pre-publication hardening phase.

This operation does not modify scientific code, frozen protocol rules,
analysis parameters, estimators, thresholds, scientific results, or
checkpoint semantics.

### Licensing structure

Software licensing:

`Apache License 2.0`

Repository software explicitly covered by the project software license
is governed by the root-level:

`LICENSE`

Original project documentation, methodological descriptions, and
scientific text are designated:

`CC BY 4.0`

except where otherwise stated or where the project does not hold the
necessary rights.

External datasets, raw neurophysiological data, third-party materials,
and materials carrying separate licensing terms are not relicensed by
the Brain Model repository.

Historical and provenance artifacts are retained for reproducibility and
auditability. Their presence in the repository does not by itself imply
relicensing under Apache-2.0 or CC BY 4.0.

### Repository artifacts

The licensing package introduces or updates:

- `LICENSE`
- `THIRD_PARTY_NOTICES.md`
- `README.md`
- `docs/MIGRATION_LEDGER.md`

`README.md` records the repository-level licensing boundary.

`THIRD_PARTY_NOTICES.md` records third-party dependency, external-data,
historical/provenance, and relicensing boundaries.

### Third-party dependencies

The current software dependency review identified use of third-party
Python packages including:

- NumPy
- pandas
- SciPy

These dependencies remain subject to their respective licenses.

No third-party dependency is relicensed by the Brain Model repository.

Exact dependency versions and environment specifications remain subject
to the separate environment-freeze operation.

### External and raw data

Raw or externally sourced datasets are not transferred into the Brain
Model licensing scheme merely because they are referenced by identifiers,
hashes, manifests, provenance records, configurations, or scientific
documentation.

Original data-source terms continue to govern those materials.

### Scientific impact

`NONE`

Scientific code modification:

`NONE`

Protocol modification:

`NONE`

Amendment-002 semantic modification:

`NONE`

G1 reopening:

`NO`

Full G2 execution:

`NO`

Scientific status remains:

`FULL_G2_NOT_RUN / G1_UNCHANGED`

### Repository phase

`ACTIVE / PRE-PUBLICATION HARDENING`

Licensing-package preparation and repository publication operations are
administrative/repository-governance operations and must not be
interpreted as scientific validation or execution of the prespecified
full G2 analysis.

### Status

`LICENSE_PACKAGE_INTEGRATED`

Final publication readiness remains dependent on completion of the
remaining pre-publication hardening gates.
