# Brain Model — Migration Ledger

**Project:** Brain Model (BM-2026)  
**Repository:** brain-model  
**Canonical branch:** main  
**Migration status:** IN PROGRESS (repository phase `ACTIVE / PRE-PUBLICATION HARDENING`)  
**Purpose:** controlled migration of Brain Model artifacts into the canonical Git repository.  
**Last updated:** 2026-10-06

## 1. Migration rule

No historical package or analysis directory is copied wholesale into the canonical source tree.

Every artifact must be classified before migration as one of:

- **CURRENT** — current canonical project state or active analysis
- **SOURCE** — executable scientific source code
- **TEST** — validation, regression, smoke, or integrity test
- **CONFIG** — frozen configuration or preregistration contract
- **GENERATED** — reproducible output generated from source/configuration
- **PROVENANCE** — audit, execution, lineage, checksum, or historical record
- **SUPERSEDED** — retained only for history/reproducibility
- **EXTERNAL/RAW** — external or raw data; referenced but not committed unless explicitly approved

## 2. Current ST44 and post-lock implementation/diagnostic lineage

Current verified lineage:

1. BM-A011 R3
2. BM-A027 preregistration / BM-CHALLENGE-001
3. Amendment-001
4. BM-A028 G0/G1 decision
5. BM-A029 G2 implementation
6. BM-A030 resumable G2 runner
7. BM-A031 candidate corrective G2 patch
8. BM-A027 Amendment-002 (pre-execution undefined-transition-row rule)
9. BM-A031 Rev2 Amendment-002-compatible implementation
10. BM-A032 positive-control / injection-recovery diagnostic

The locked BM-A011 R3 and G1 result must not be silently modified by later analyses.

BM-A031 and BM-A032 are post-lock implementation/diagnostic developments. Their existence does not alter the frozen BM-A011 R3 result or reopen G1.

## 3. Artifact ledger

Full SHA-256 values are listed in section 16; the table shows the first eight hexadecimal digits.

| Artifact | Classification | Status | Target / policy | SHA-256 |
|—|—|—|—|—|
| README.md | CURRENT | MIGRATED; rewritten 2026-10-06 | repository root | — |
| CHANGELOG.md | CURRENT / PROVENANCE | MIGRATED | repository root | — |
| .gitignore | CONFIG | MIGRATED | repository root | — |
| CITATION.cff | CURRENT | ADDED 2026-10-06 | repository root | — |
| LICENSE, NOTICE, THIRD_PARTY_NOTICES.md, docs/LICENSE-DOCS.md | CURRENT | LICENSING PACKAGE (2026-10-04; completed 2026-10-06) | repository root; docs/ | LICENSE `cfc7749b` |
| docs/PROJECT_STATUS.md | CURRENT | MIGRATED | docs/ | — |
| docs/MIGRATION_LEDGER.md | CURRENT / PROVENANCE | CURRENT | docs/ | — |
| BM-A011 R3 scientific package | SOURCE / PROVENANCE | FROZEN — NOT YET MIGRATED | classify contents before migration | ZIP `9ab675e3` |
| BM-A011 R3 outputs | GENERATED | FROZEN — NOT YET MIGRATED | results/ after manifest verification | result archive `20b6e95d` |
| BM-A027 preregistration | CONFIG / PROVENANCE | FROZEN / MIGRATED / BYTE-INTEGRITY VERIFIED (2026-10-06) | docs/provenance/BM-A027_PREREGISTRATION.md (library file BM_31_CHALLENGE_001_PREREG_BM-A027_2026-09-29.md) | `f6403115` |
| BM-A027 Amendment-001 | CONFIG / PROVENANCE | FROZEN / MIGRATED / BYTE-INTEGRITY VERIFIED (2026-10-06) | docs/provenance/ | `ccf4a7b5` |
| BM-A027 Amendment-002 | CONFIG / PROVENANCE | FROZEN / MIGRATED (first recorded in Git, `8609c1f`) | docs/provenance/; pre-execution G2 undefined-transition-row policy | `20d4aa95` |
| BM-A027 frozen config | CONFIG / PROVENANCE | FROZEN / MIGRATED / BYTE-INTEGRITY VERIFIED | docs/provenance/ | `b15436dc` |
| BM-A028 G0/G1 decision | PROVENANCE / GENERATED | FROZEN — NOT YET MIGRATED | docs/provenance/ or results/ | JSON `e37c36d0`, MD `39c73abc` |
| BM-A029 G2 replay | SOURCE | SUPERSEDED FOR EXECUTION — NOT MIGRATED | archive/provenance after verification | `961ab5f9` (code package v1.0 copy) |
| BM-A030 resumable runner | SOURCE / PROVENANCE | SUPERSEDED FOR EXECUTION — NOT MIGRATED | archive/provenance after verification | `669693c4` |
| BM-A031 original patched G2 runner | SOURCE / PROVENANCE | SUPERSEDED BY BM-A031 REV2 — NOT MIGRATED | preserve in provenance/history; do not use for full G2 | `53ea3af0` |
| BM-A031 Rev2 patched G2 runner | SOURCE | CANONICAL since 2026-10-03 (`311d0e5`); PROTOCOL_COMPATIBILITY_VERIFIED / CORE_MATH_VERIFIED / AMENDMENT002_REPORTING_COMPLIANT / CHECKPOINT_V3_CONTRACT_VERIFIED / FULL_G2_NOT_RUN | src/ (canonical) + archive/provenance/ (byte-identical copy) | `f1619b28` |
| BM-A031 Rev2 regression test | TEST | CANONICAL — targets the src/ runner; 7/7 PASS | tests/ | `1a11a9dc` |
| BM-A031 original patch note | PROVENANCE | HISTORICAL — NOT MIGRATED | retain unchanged; refers to earlier runner identity | — |
| BM-A031 Rev2 Amendment-002 compatibility record | PROVENANCE | CURRENT — MIGRATED (`c40b814`); correction note 2026-10-06 | docs/provenance/ | — |
| BM-CI-CERT-001 v0.2 CI contract | TEST / PROVENANCE | LOCAL PASS 2026-10-05; REMOTE NOT YET VERIFIED | tools/, .github/workflows/ci-cert.yml, requirements-ci.txt, CONTRACT_SHA256.txt; delivery record in docs/provenance/ci/BM-CI-CERT-001_v0.2/ | verifier `ea7861bf` |
| BM-A032 frozen protocol | CONFIG / PROVENANCE | CURRENT DIAGNOSTIC — NOT MIGRATED | configs/ + docs/provenance/ after verification | — |
| BM-A032 Phase-A runner | SOURCE / TEST | CURRENT DIAGNOSTIC — NOT MIGRATED | tests/ or scripts/ after verification | — |
| BM-A032 Phase-A outputs | GENERATED | REVIEW — NOT MIGRATED | results/diagnostics/ | — |
| BM-A032 execution record | PROVENANCE | CURRENT — NOT MIGRATED | docs/provenance/ | — |
| BM ST44 R3 preprint v1.0 (2026-10-02) | PROVENANCE / DOCUMENT | HISTORICAL — a new preprint is in preparation (2026-10-06) | not migrated as the current publication; the new preprint goes to docs/preprint/ when available | PDF `3e70d1db` |
| BM-PKG-001 | SUPERSEDED / PROVENANCE | SUPERSEDED | archive only | — |
| BM-PKG-002 | PROVENANCE | HISTORICAL REPRODUCIBILITY BASELINE | archive/provenance; not canonical source | — |
| Sleep-EDF / ST44 raw EDF data | EXTERNAL/RAW | EXTERNAL | DO NOT COMMIT | — |
| External HDF5/raw datasets | EXTERNAL/RAW | EXTERNAL | DO NOT COMMIT | — |

## 4. Scientific lock

The following BM-A011 R3 properties remain frozen during migration:

- cohort: 19 participants / 38 recordings
- surrogate count: B = 1999 per recording × variant
- master seed: 20260921
- support: contiguous N2 runs
- transitions never cross N2-run boundaries
- statistic: T_cs on common target support
- primary nulls:
  - common_phase_run
  - epochwise_common_phase
- sensitivity null:
  - independent_channel_phase

G1 is closed.

Later code migration, G2 diagnostics, positive controls, repository restructuring, documentation changes, or implementation corrections must not retroactively alter the locked G1 result.

## 5. Current G1 state

Locked status:

`RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS`

This is a bounded statistical result.

It must not be promoted to claims that:

- neural memory is absent;
- temporal dependence is absent;
- nonlinear dynamics are absent;
- every Brain Model representation is falsified;
- preserved spectra or phase structure explain all relevant neural dynamics.

The result applies to the frozen ST44 operator, statistic, cohort, support definition and prespecified common-phase null hierarchy.

## 6. BM-A027 operative preregistration state

The operative BM-A027 preregistration consists of:

1. BM-A027 / BM-CHALLENGE-001 v1.0;
2. BM-A027 Amendment-001;
3. BM-A027 Amendment-002 for the pre-execution G2 undefined-transition-row implementation rule;
4. BM-A027 frozen machine-readable configuration.

Where Amendment-001 conflicts with the original v1.0 document, Amendment-001 controls for the scope it amends. Amendment-002 controls the subsequently frozen G2 undefined-transition-row implementation rule for its stated scope.

The operative primary chain remains:

G0 — execution integrity → G1 — inherited frozen R3 raw-signal null gate → G2 — mandatory lower-order diagnostic context → G3 — continuous-domain temporal value-added gate

External replication remains necessary for cross-dataset or general claims.

The representation/spectral multiverse originally described as G4 is not part of the primary G0–G3 ST44 chain after Amendment-001.

G2 defines:

- D_occ
- D_self
- D_M1
- z_T
- participant-cluster bootstrap B = 10000
- seed = 20260929

Amendment-002 additionally freezes, before full G2 execution:

- state order: LL, LH, HL, HH;
- zero-outgoing transition rows as undefined rather than artificial zero distributions;
- NaN/null representation of undefined rows;
- finite-only null aggregation for defined values;
- no artificial discrepancy contribution from wholly undefined observed rows in D_self/D_M1;
- no renormalization of q_obs after excluding undefined comparisons;
- checkpoint provenance including schema, runner SHA-256, state order, undefined-row policy and applicable amendment identifier;
- explicit reporting of undefined-row occurrence and null availability.

Amendment-002 does not reopen G1 and does not convert G2 into a new confirmatory hypothesis test.

## 7. BM-A031 state

BM-A031 is a post-preregistration corrective implementation of the G2 analysis layer. It does not reopen or modify G1.

The original BM-A031 patch is retained as historical provenance and has been superseded for prospective execution by BM-A031 Rev2.

Current BM-A031 Rev2 state:

- PROTOCOL_COMPATIBILITY_VERIFIED
- CORE_MATH_VERIFIED
- AMENDMENT002_REPORTING_COMPLIANT
- CHECKPOINT_V3_CONTRACT_VERIFIED
- FULL_G2_NOT_RUN
- G1_UNCHANGED

BM-A031 Rev2 includes:

- state order: LL, LH, HL, HH;
- explicit undefined handling for transition rows with no observed outgoing transitions;
- finite-only null aggregation;
- Amendment-002-compatible D_self and D_M1 handling without artificial zero-distribution mismatch;
- checkpoint schema V3;
- runner SHA-256 in checkpoint contract;
- state-order, undefined-row-policy and Amendment-002 provenance in the contract;
- fail-closed behavior for incompatible checkpoint contracts;
- explicit reporting of observed undefined-row counts/frequencies, null availability and affected recording × variant cases;
- repository-relative regression-test targeting of the canonical src/ runner.

Verified BM-A031 Rev2 runner SHA-256:

`f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b`

Current Rev2 regression-test SHA-256:

`1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2`

Historical regression-test SHA-256 values (path-only changes): `eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d` (before the path correction) and `c126618eaa22d2e1587efa3f6c469cf60e8c85563bbdf5f4e262f955cd9178ff` (archive path, 2026-10-03).

The original BM-A031 provenance note must not be silently rewritten to imply that it described Rev2. A separate Rev2 Amendment-002 compatibility record preserves the revision lineage.

BM-A031 Rev2 was promoted to canonical src/ on 2026-10-03 (commit `311d0e5`) as a byte-identical copy of the archived runner. Full G2 has not been executed.

Operational rule: production G2 runs on the complete locked inventory only. The runner labels every run without `—smoke-B` as `G2_COMPLETE`, including a run restricted with `—recordings` (observed in a synthetic end-to-end harness on 2026-10-06). A subset run must never be reported as full G2.

## 8. BM-A032 state

BM-A032 is a diagnostic positive-control / injection-recovery analysis.

Current state:

- REVIEW
- SEQUENCE_LEVEL_DIAGNOSTIC_COMPLETE
- RAW_SIGNAL_PHASE_B_NOT_RUN

Phase-A diagnostic:

- lambda = 0 rejection/recovery: 0.048
- lambda = 1 recovery: 0.000
- monotone adjacent pairs: 7/8

The first injection construction therefore did not validate as a suitable positive-control family.

BM-A032 Phase A must not be described as an empirical Sleep-EDF power estimate.

The next scientific step is diagnosis/revision of the positive-control generator before using it to make power claims.

BM-A032 does not alter the locked G1 result.

## 9. Historical packages

BM-PKG-001 is superseded.

BM-PKG-002 is retained as a historical reproducibility baseline.

BM-PKG-002 must not be treated as the current scientific state of Brain Model and must not be unpacked wholesale into the canonical source tree.

Historical packages may be retained under archive/provenance or referenced by checksum.

Historical reproducibility artifacts and current canonical implementation must remain distinguishable.

## 10. Raw-data policy

Raw or externally distributed datasets are not committed to Git.

The repository should contain instead, where appropriate:

- dataset identifiers
- acquisition instructions
- expected filenames
- checksums where legally and technically appropriate
- preprocessing contracts
- provenance records

No raw EDF/HDF5 dataset is migrated merely because it was used by a historical Brain Model analysis.

The Sleep-EDF Database Expanded v1.0.0 is distributed by PhysioNet under ODC-By 1.0; source, licence, required notice and citations are recorded in THIRD_PARTY_NOTICES.md.

## 11. Migration verification

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

## 12. Planned canonical structure

The intended structure is:

```text
brain-model/
├── README.md
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE
├── NOTICE
├── THIRD_PARTY_NOTICES.md
├── .gitignore
├── .github/workflows/
├── docs/
│   ├── PROJECT_STATUS.md
│   ├── MIGRATION_LEDGER.md
│   ├── LICENSE-DOCS.md
│   ├── provenance/
│   └── preprint/
├── src/
├── tests/
├── tools/
├── scripts/
├── configs/
├── results/
│   └── diagnostics/
└── archive/
    └── provenance/
```

Directories are created only when the first classified artifact is ready for them.

Empty directory structure is not treated as a migration result because Git does not track empty directories.

## 13. Current migration gate

Current repository phase:

`ACTIVE / PRE-PUBLICATION HARDENING`

Completed migration gates:

- REPOSITORY_BOOTSTRAP
- PROJECT_STATUS_COMMITTED
- MIGRATION_LEDGER_CREATED
- BM-A027_PREREGISTRATION_BUNDLE_MIGRATED
- BM-A027_AMENDMENT002_FROZEN_AND_MIGRATED
- BM-A027_FROZEN_CONFIG_BYTE_INTEGRITY_VERIFIED
- BM-A031_REV2_PROTOCOL_COMPATIBILITY_VERIFIED
- BM-A031_REV2_AMENDMENT002_REPORTING_VERIFIED
- BM-A031_REV2_CHECKPOINT_V3_CONTRACT_VERIFIED
- BM-A031_REV2_CANONICAL_SOURCE_PROMOTION (2026-10-03, `311d0e5`)
- BM-A031_CANONICAL_TEST_PATH_SYNC (2026-10-03)
- BM-2026_PREPUBLICATION_LICENSING_PACKAGE (2026-10-04; completed 2026-10-06)
- BM-CI-CERT-001_V0.2_LOCAL_PASS (2026-10-05)
- BM-A027_PREREGISTRATION_BYTE_INTEGRITY_VERIFIED (2026-10-06)

Previous gates:

- BM-A031_PROTOCOL_COMPATIBILITY_PENDING — resolved by Amendment-002 + BM-A031 Rev2
- BM-A031_REV2_PRE_CANONICALIZATION_PROVENANCE_AND_CLEAN_CHECKOUT_VERIFICATION — resolved by canonical promotion and test-path synchronization (2026-10-03)
- BM-A031_CANONICALIZATION_BUNDLE_COMMIT_AND_REMOTE_VERIFICATION — bundle committed; remote verification deferred (2026-10-04)

Current gate:

`BM-A031_PREPUBLICATION_REPOSITORY_HARDENING`

Remaining before an archival release: migration or deposit of the BM-A011 R3 package, the R3 outputs and the BM-A028 decision record; full G2 execution; remote CI verification; DOI of the new preprint.

Full G2 must remain unexecuted until the intended executable identity and its applicable protocol/provenance are unambiguous.

## 14. Migration integrity note

Migration into Git is an archival and software-governance operation.

A Git commit does not by itself:

- validate a scientific result;
- promote a candidate implementation to canonical scientific status;
- convert an exploratory analysis into a preregistered analysis;
- reopen a closed inferential gate;
- change the interpretation of BM-A011 R3.

Scientific status is determined by the applicable frozen protocol, validated execution record and documented analysis lineage.

## 15. Current status summary

| Item | Status |
|—|—|
| Repository | ACTIVE / PRE-PUBLICATION HARDENING |
| BM-A011 R3 | FROZEN / G1 CLOSED |
| BM-A027 | FROZEN PREREGISTRATION + AMENDMENT-001 + AMENDMENT-002 / MIGRATED / v1.0, AMENDMENT-001 AND CONFIG BYTE-INTEGRITY VERIFIED |
| BM-A031 Rev2 | CANONICAL / PROTOCOL_COMPATIBILITY_VERIFIED / CORE_MATH_VERIFIED / AMENDMENT002_REPORTING_COMPLIANT / CHECKPOINT_V3_CONTRACT_VERIFIED / FULL_G2_NOT_RUN / G1_UNCHANGED |
| BM-A032 | REVIEW / SEQUENCE_LEVEL_DIAGNOSTIC_COMPLETE / RAW_SIGNAL_PHASE_B_NOT_RUN |
| CI contract | LOCAL PASS / REMOTE NOT YET VERIFIED |

Next decision: migrate or deposit the BM-A011 R3 package, the R3 outputs and the BM-A028 decision record, then decide on the release form (protocol snapshot before full G2, or archival release after full G2).

## 16. Integrity register (SHA-256)

### Files in this repository

| File | SHA-256 |
|—|—|
| src/BM-A031_G2_PATCHED_RUNNER.py | `f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b` |
| archive/provenance/BM-A031_G2_PATCHED_RUNNER.py | `f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b` |
| tests/test_bm_a031_amendment002_rev2.py | `1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2` |
| docs/provenance/BM-A027_PREREGISTRATION.md | `f6403115755901861b8e202495841fb38d126a4c89ced2f80241ca569573fb90` |
| docs/provenance/BM-A027_AMENDMENT_001_PREOUTCOME_SOURCE_CONSISTENCY_2026-09-29.md | `ccf4a7b5fedacdf417fcb048c5639220a4116cc4e0c3c7168462d7cc8c31497e` |
| docs/provenance/BM-A027_AMENDMENT_002_G2_UNDEFINED_TRANSITION_ROWS.md | `20d4aa957f995182801e332fdf0ed00abadd079cb4366623695918f0b86d7a9f` |
| docs/provenance/BM-A027_CHALLENGE001_FROZEN_CONFIG.json | `b15436dca3970fb680dde7b71bd03e7ebef1c309de351907a1645ee5b4fa04b3` |
| requirements-ci.txt | `2905ba50505ca0a4dd03ae415e4e8e84dedb4d4ef560fa8e051e4306aa681553` |
| .github/workflows/ci-cert.yml | `a6c8644c417419fcfba2a5d155f992f5944fbebcf087e59db224a2b9dc80c968` |
| tools/verify_ci_contract.py | `ea7861bf6a7eab5c3e7f9e0e5bed877b396f3ae83916dfa39e8e82086fa9f2d6` |
| LICENSE (canonical Apache License 2.0 text) | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |

### Frozen artifacts referenced but not yet migrated

| Artifact | SHA-256 |
|—|—|
| BM-A011 R3 scientific package (BM-A011_STEP3_FULL_RAW_SIGNAL_V3CS_R3_2026-09-26.zip) | `9ab675e3acd157b21845f5f242b43274337c6cb4f5121efc59ad03a84110414f` |
| BM-A011 R3 final result archive | `20b6e95d482c3371ce5b95ee44f861b6f39f327dbbd61d40fe276e674c6726f3` |
| BM-A028_G0_G1_DECISION.json | `e37c36d089afd09ede83b1949b367552fa1d03c00530f4c0a5680deef17acde2` |
| BM-A028_G0_G1_DECISION.md | `39c73abcbee30408b677e5337aae015fc6222a5e77cc60657916f56dd78292c4` |
| BM-A029_G2_LOWER_ORDER_REPLAY.py (code package v1.0 copy) | `961ab5f9fb14b1ac9d55c1dd63e8bc6fbdae761cc10210fc68cc1336d12651fe` |
| BM-A030_G2_SMART_RESUME_CHECKPOINT_RUNNER.py | `669693c4d36369c835fe8e7caa84197eb4c8d88b51b327f8be76d9c0132c3373` |
| BM-A031 original patched runner | `53ea3af023e20b22ce8dbe6c320fa1f57c320854c96e3d29803ce79c6c6d2ff1` |
| BM-A031 Amendment-002-aware intermediate runner | `abef8acdbfc6f1f9269ee60f507984b177b219013249bd2a2793d7514de52538` |
| BM_ST44_R3_CODE_PACKAGE_v1_0_2026-10-02.zip | `c0a461390f55e96469b722ff39a04f6e18955bd0904f827244fc1267554caa81` |
| BM_ST44_R3_PREPRINT_v1_0_2026-10-02.pdf (historical) | `3e70d1dbd3cb9d847a52d5ce0c28cbd13cad3800f9ed75de6241583588717f89` |

### Project-library timestamps (Google Drive metadata, UTC)

| Library file | Drive file ID | Created | Modified | Size (B) |
|—|—|—|—|—|
| BM_31_CHALLENGE_001_PREREG_BM-A027_2026-09-29.md | `1oQnZ1AvXtOSgg2CYgQIr3b-g2xcVHDcD` | 2026-09-29T19:58:11Z | never | 17,307 |
| BM-A027_CHALLENGE001_FROZEN_CONFIG.json | `1VBVe4Sml5BPIPB8QN55qYyQKuPf4G8cI` | 2026-09-29T19:58:18Z | never | 3,524 |
| BM-A027_AMENDMENT_001_PREOUTCOME_SOURCE_CONSISTENCY_2026-09-29.md | `1GpOGy_lN0ylZPOpJp4T0Gy3Wbrjh4nAm` | 2026-09-29T20:01:57Z | never | 5,166 |
| BM-A028_G0_G1_DECISION.json | `1fhEjQS00oMi5OMzAMMOZQhNL0oW5iKj1` | 2026-10-02T04:05:24Z | 2026-10-02T06:14:14Z | 713 |
| BM-A027_LOWER_ORDER_SUMMARY.json (BM-A029 smoke, `SMOKE_ONLY`, B = 2) | `1YgvL05dez2aaNT5pIhGaR9LqRQ5Q5djK` | 2026-10-02T07:25:04Z | never | 529 |

Drive metadata are recorded by Google but are not a public registry; they can be shown to reviewers by sharing the files view-only.

## 17. History notes

These notes record repository history that is not described elsewhere. None of it changes scientific status.

- `a136e45` (2026-09-30) added `BRAIN_MODEL_GITHUB_FIRST_UPLOAD_2026-09-30`, an iOS Files bookmark (binary property list, SHA-256 `d3b0aebbb0ad0fcbc13b4f6b8ffefb49d59ce3a88ba47deb96c273a4f4467457`) without scientific content; removed in `ec32b17`.
- `89ad55e` and `52cebf2` (2026-09-30) added early copies of BM-A004 (`brain-model/BM-A004__…AUDITED.py` and `brain-model/shell-script.py`, both byte-identical to the frozen operator, SHA-256 `e82a9fba5cba5892145a7d8401e15552a10efe2ef35654181551be9d04bd0080`), the BM-A005 orchestrator (`8d0b74d7bb466456dfb05928e605621e5f7ee6266c9fd16cb63c95a33916e6f5`) and a BM-A028 Colab notebook (`c1e6b109e88c4a42278df93da9ca135eaefe347f944b6c69a41fa6c9da0a5b8d`); removed as misplaced in `955504b` (2026-10-02).
- `b10df94` (2026-10-02T20:44:56+02:00) added a corrupted copy of the Amendment-002-aware intermediate runner (SHA-256 `08fc4517aedf9c0b4ec0f00866eaae778747273df51cd00a604b5eeedaada326`): the shebang lacks `#`, so the file does not compile, and it still carries BM-A030 labels. It was replaced by Rev2 in `f34d37a` (2026-10-02T21:04:49+02:00) and was never used for execution.
- The compatibility record cites commit `a6a6d01`, which does not exist in the repository history; the path correction is in `5d0fbb4`. A dated correction note was added to the record on 2026-10-06.

## 2026-10-04 — Pre-publication licensing package

### Operation

`BM-2026_PREPUBLICATION_LICENSING_PACKAGE`

### Scope

Repository licensing and publication-governance update performed during the pre-publication hardening phase.

This operation does not modify scientific code, frozen protocol rules, analysis parameters, estimators, thresholds, scientific results, or checkpoint semantics.

### Licensing structure

Software licensing:

`Apache License 2.0`

Repository software explicitly covered by the project software license is governed by the root-level:

`LICENSE`

Original project documentation, methodological descriptions, and scientific text are designated:

`CC BY 4.0`

except where otherwise stated or where the project does not hold the necessary rights.

External datasets, raw neurophysiological data, third-party materials, and materials carrying separate licensing terms are not relicensed by the Brain Model repository.

Historical and provenance artifacts are retained for reproducibility and auditability. Their presence in the repository does not by itself imply relicensing under Apache-2.0 or CC BY 4.0.

### Repository artifacts

The licensing package introduces or updates:

- `LICENSE`
- `THIRD_PARTY_NOTICES.md`
- `README.md`
- `docs/MIGRATION_LEDGER.md`

`README.md` records the repository-level licensing boundary.

`THIRD_PARTY_NOTICES.md` records third-party dependency, external-data, historical/provenance, and relicensing boundaries.

### Third-party dependencies

The current software dependency review identified use of third-party Python packages including:

- NumPy
- pandas
- SciPy

These dependencies remain subject to their respective licenses.

No third-party dependency is relicensed by the Brain Model repository.

Exact dependency versions and environment specifications remain subject to the separate environment-freeze operation.

### External and raw data

Raw or externally sourced datasets are not transferred into the Brain Model licensing scheme merely because they are referenced by identifiers, hashes, manifests, provenance records, configurations, or scientific documentation.

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

Licensing-package preparation and repository publication operations are administrative/repository-governance operations and must not be interpreted as scientific validation or execution of the prespecified full G2 analysis.

### Status

`LICENSE_PACKAGE_INTEGRATED`

Final publication readiness remains dependent on completion of the remaining pre-publication hardening gates.

Note (2026-10-06): the licence file was committed on 2026-10-04 as `LICENCE` with a truncated appendix. It was renamed to `LICENSE` and replaced by the complete canonical text on 2026-10-06.

## 2026-10-06 — Publication-readiness corrections

### Operation

`BM-2026_PUBLICATION_READINESS_CORRECTIONS`

### Scope

Documentation, licensing, provenance records and repository layout. No scientific code, regression test, frozen protocol rule, estimator, threshold, checkpoint contract or CI contract file was changed.

### Changes

- README rewritten (status, contents, verification commands, data and attribution, prespecification timeline, release policy, licensing).
- `CITATION.cff`, `NOTICE` and `docs/LICENSE-DOCS.md` added; `LICENCE` renamed to `LICENSE` and replaced by the complete canonical Apache-2.0 text.
- THIRD_PARTY_NOTICES.md extended with the Sleep-EDF source, licence, notice and citations, and the dependency licences.
- BM-A027 v1.0 and Amendment-001 replaced by the byte-exact frozen originals (word-level identical to the previous copies, which had lost their Markdown markup).
- Correction note appended to the BM-A031 Rev2 compatibility record (commit reference `a6a6d01`).
- PROJECT_STATUS.md and this ledger brought up to date; integrity register (section 16) and history notes (section 17) added.
- BM-CI-CERT-001 v0.2 delivery records moved unchanged to `docs/provenance/ci/BM-CI-CERT-001_v0.2/`.
- Publication: preprint v1.0 is historical; a new preprint is in preparation.

Frozen documents were left byte-unchanged even where cosmetic defects exist (for example, a stray backtick at the end of the Amendment-002 change-log line).

### Scientific impact

`NONE`

Scientific status remains:

`FULL_G2_NOT_RUN / G1_UNCHANGED`
