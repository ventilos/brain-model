# Brain Model (BM-2026)

Analysis code, prespecified analysis plans and provenance records for the Brain Model project (BM-2026): a retrospective, falsification-oriented test of second-order temporal structure in N2 sleep EEG from the Sleep-EDF Expanded sleep-telemetry (ST) recordings.

**Author:** Łukasz Westphal, independent researcher, Poland · ORCID [0009-0006-2998-1318](https://orcid.org/0009-0006-2998-1318)  
**Repository status:** `ACTIVE / PRE-PUBLICATION HARDENING`  
**Scientific status:** `FULL_G2_NOT_RUN / G1_UNCHANGED` (details: [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md))

## Scientific status

| Gate | Analysis | State |
|—|—|—|
| G0 — execution integrity | BM-A011 R3, decision BM-A028 | PASS (38/38 checkpoints, all 12 production audits) |
| G1 — raw-signal surrogate null | BM-A011 R3, decision BM-A028 | FAIL → locked claim state `RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS` |
| G2 — lower-order diagnostics | BM-A027 + Amendment-002, runner BM-A031 Rev2 | Implementation verified; **full G2 not run** |
| G3 — continuous-domain value added | BM-A027 Amendment-001 | Not run |

Empirical group p-values of the frozen G1 test: 0.8773 (`common_phase_run`) and 0.1264 (`epochwise_common_phase`); the sensitivity null `independent_channel_phase` gave 0.1152.

These results are bounded to the frozen ST44 operator, statistic, cohort and surrogate hierarchy. Nothing in this repository establishes a biological mechanism, a universal field, consciousness, causality, a treatment effect or clinical validity.

## Contents

| Path | What it is |
|—|—|
| `src/BM-A031_G2_PATCHED_RUNNER.py` | Canonical G2 runner, BM-A031 Rev2 |
| `archive/provenance/` | Byte-identical archived copy of the runner (provenance) |
| `tests/` | Regression tests for the Amendment-002 semantics (7 tests) |
| `tools/verify_ci_contract.py` | Fail-closed CI contract BM-CI-CERT-001 v0.2 |
| `docs/provenance/` | BM-A027 analysis plan, Amendments 001 and 002, frozen configuration, BM-A031 Rev2 compatibility record, CI certification record |
| `docs/PROJECT_STATUS.md` | Current state, gates and open items |
| `docs/MIGRATION_LEDGER.md` | Classification, status and SHA-256 of every project artifact |
| `CHANGELOG.md` | Repository change history |

### Not yet in this repository

The following frozen artifacts are referenced by hash but have not been migrated yet (see [docs/MIGRATION_LEDGER.md](docs/MIGRATION_LEDGER.md)):

- BM-A011 R3 scientific package — operator BM-A004, orchestrator BM-A011, download receipt; ZIP SHA-256 `9ab675e3acd157b21845f5f242b43274337c6cb4f5121efc59ad03a84110414f`;
- BM-A011 R3 result archive — recording and group summaries, audits; ZIP SHA-256 `20b6e95d482c3371ce5b95ee44f861b6f39f327dbbd61d40fe276e674c6726f3`;
- BM-A028 G0/G1 decision record.

The G2 runner loads BM-A004 and BM-A011 from `—package-root` and the R3 outputs from `—r3-root`, so a full G2 run is not possible from this repository alone. These artifacts will be migrated or deposited before an archival release.

## Quick verification

Requires Python 3.11 or newer.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python src/BM-A031_G2_PATCHED_RUNNER.py —checkpoint-selftest
```

These commands run the regression tests and the checkpoint self-test. They do not reproduce G1 and do not execute G2.

The frozen CI contract additionally requires exactly Python 3.13.5 and the pinned CI environment:

```bash
python -m pip install -r requirements-ci.txt
python tools/verify_ci_contract.py
```

Continuous integration runs `.github/workflows/tests.yml` (Python 3.11, `requirements.txt`) and `.github/workflows/ci-cert.yml` (Python 3.13.5, frozen hash contract). A passing CI contract certifies the BM-A031 Rev2 contract only; it is not a full-project reproducibility check.

A full G2 run additionally needs the BM-A011 R3 package and outputs listed above, the raw EDF files, and the R3 runtime pins `mne==1.11.0` and `requests==2.32.5`. Production G2 must be run on the complete locked inventory: the runner labels any run without `—smoke-B` as `G2_COMPLETE`, including a run restricted with `—recordings`.

## Data

Source: **Sleep-EDF Database Expanded, version 1.0.0** (PhysioNet), sleep-telemetry (ST) subset. The frozen pipeline uses EEG Fpz-Cz, EEG Pz-Oz, horizontal EOG and submental EMG at 100 Hz, together with the expert hypnograms. The ST study recorded one temazepam night and one placebo night per participant; this project does not test a treatment effect.

Locked analysis cohort: 19 participants / 38 recordings; subjects 21, 22 and 24 were excluded as pilot subjects before production inference. The participant is the population-level inferential unit.

Raw data are not stored in this repository and are not redistributed. Obtain them from PhysioNet: <https://physionet.org/content/sleep-edfx/1.0.0/>. The database is made available under the Open Data Commons Attribution License v1.0 (ODC-By 1.0). Any derived data shared from this project must carry the notice: *”Contains information from Sleep-EDF Database Expanded which is made available under the ODC Attribution License.”*

Please cite:

- Kemp B. Sleep-EDF Database Expanded (version 1.0.0). PhysioNet. <https://doi.org/10.13026/C2X676>
- Kemp B, Zwinderman AH, Tuk B, Kamphuisen HAC, Oberyé JJL. Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG. *IEEE Trans Biomed Eng.* 2000;47(9):1185–1194. <https://doi.org/10.1109/10.867928>
- Goldberger AL, Amaral LAN, Glass L, et al. PhysioBank, PhysioToolkit, and PhysioNet: components of a new research resource for complex physiologic signals. *Circulation.* 2000;101(23):e215–e220. <https://doi.org/10.1161/01.CIR.101.23.e215>

## Prespecification and provenance

The operative analysis plan is BM-A027 v1.0 with Amendment-001 and Amendment-002 ([docs/provenance/](docs/provenance/)). The repository copies of BM-A027 v1.0, Amendment-001 and the frozen configuration are byte-identical to the frozen files in the project library (SHA-256 in [docs/MIGRATION_LEDGER.md](docs/MIGRATION_LEDGER.md)).

| Time (UTC) | Event | Source of the timestamp |
|—|—|—|
| 2026-09-29 19:58:11 | BM-A027 v1.0 created in the project library; never modified since | Google Drive file metadata |
| 2026-09-29 20:01:57 | Amendment-001 created; never modified since | Google Drive file metadata |
| 2026-10-02 04:05:24 | BM-A028 G0/G1 decision record created — first record of the G1 outcome | Google Drive file metadata |
| 2026-10-02 16:50:31 | BM-A027 v1.0 and Amendment-001 first committed to this repository (`8b5b004`) | Git commit date |
| 2026-10-02 17:16:28 | Amendment-002 first committed (`8609c1f`), before any full-G2 execution | Git commit date |

Google Drive metadata are recorded by Google but are not a public registry, and Git commit dates are set by the committer. The first independently verifiable public timestamp of these documents will be the first public release of this repository.

## Related publication

ST44 preprint v2.6 (2026-10-09): Read the preprint (PDF).

This is an author preprint, not a peer-reviewed publication. No DOI has been assigned.

The frozen G1 conclusion remains RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS. The full G2 analysis has not been run (FULL_G2_NOT_RUN).

Publishing the preprint does not constitute independent reproduction of the scientific results. A DOI may be added following a separate archival deposit.

## How to cite

Use the metadata in [`CITATION.cff`](CITATION.cff) (GitHub: „Cite this repository”). Cite the dataset as listed under [Data](#data).

## Release policy

Development versions may change. GitHub holds the development history; Zenodo will hold immutable archival releases with DOIs.

An archival release of results is created only after:

1. completion of the prespecified analysis,
2. a final integrity audit,
3. reproducibility verification,
4. freezing of code and manifests,
5. green CI on the release commit; otherwise the release notes must state `REMOTE_REPOSITORY_NOT_INDEPENDENTLY_VERIFIED`.

A protocol snapshot (tag `vX.Y.Z-protocol`) may be released before a prespecified analysis is executed, to give the frozen plan and the runner identity a public timestamp. A protocol snapshot reports no new results and does not change any scientific status.

## License

Copyright © 2026 Łukasz Westphal.

- Software (`src/`, `tests/`, `tools/`, `archive/`, CI workflows): Apache License 2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
- Original documentation, methodological descriptions and scientific text: CC BY 4.0 — see [`docs/LICENSE-DOCS.md`](docs/LICENSE-DOCS.md).
- External datasets, third-party software and other third-party material keep their own terms and are not relicensed — see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

Historical and provenance artifacts are retained for reproducibility and auditability; their presence does not by itself imply relicensing under Apache-2.0 or CC BY 4.0.
