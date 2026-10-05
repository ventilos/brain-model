# Brain Model

Research repository for the Brain Model (BM-2026) project.

## Status

**Work in progress / public research repository**

Current analyses are retrospective and falsification-oriented.
No result in this repository should be interpreted as establishing a biological mechanism, a universal field, consciousness, causality, or clinical validity.

## Current analysis line

The current ST44 raw-signal analysis evaluates the frozen common-support statistic using prespecified surrogate-null variants:

- `common_phase_run`
- `independent_channel_phase`
- `epochwise_common_phase`

Primary population unit: participant.

Locked retrospective holdout:
- 19 participants
- 38 recordings
- subjects 21, 22 and 24 excluded as pilot subjects

## Repository structure

```text
docs/              project documentation
src/               analysis code
analysis/          analysis specifications and reports
preregistration/   frozen analysis plans and amendments
manifests/         provenance and SHA-256 manifests
results/summary/   compact derived results
```

## Data policy

Raw EEG/PSG data are **not stored in this repository**.

The repository stores:
- source identifiers,
- provenance records,
- cryptographic hashes,
- analysis code,
- manifests,
- compact derived results.

Raw data remain in their original/restricted source locations where applicable.

## Reproducibility

Claim-bearing releases should include:

- frozen code version,
- parameter manifest,
- dependency/environment specification,
- input-data provenance,
- SHA-256 checksums,
- validation/audit outputs,
- changelog entry.

### Installation and code checks

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python src/BM-A031_G2_PATCHED_RUNNER.py —checkpoint-selftest
```

These commands install dependencies and run regression and checkpoint
self-tests. They do not reproduce the G1 analysis or execute full G2.

Local verification environment: Python 3.13.5.
CI test environment: Python 3.11. 

## Release policy

Development versions may change.

A public archival release should only be created after:
1. completion of the prespecified analysis,
2. final integrity audit,
3. reproducibility verification,
4. freezing of code and manifests.

GitHub will hold the development history.
Zenodo will be used for immutable archival releases and DOI assignment.

## License

Software in this repository is licensed under the Apache License 2.0,
except where otherwise stated.

Project documentation, methodological descriptions, and original
scientific text are licensed under the Creative Commons Attribution
4.0 International License (CC BY 4.0), except where otherwise stated.

External datasets, raw neurophysiological data, third-party materials,
and artifacts carrying separate provenance or licensing terms are not
relicensed by this repository. Their original terms continue to apply.

Historical and provenance artifacts are retained for reproducibility
and auditability. Their presence in the repository does not by itself
imply relicensing under Apache-2.0 or CC BY 4.0.

## Project

**Brain Model — BM-2026**
