# Brain Model

Research repository for the Brain Model (BM-2026) project.

## Status

**Work in progress / private research repository**

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

## Release policy

Development versions may change.

A public archival release should only be created after:
1. completion of the prespecified analysis,
2. final integrity audit,
3. reproducibility verification,
4. freezing of code and manifests.

GitHub will hold the development history.
Zenodo will be used for immutable archival releases and DOI assignment.

## Project

**Brain Model — BM-2026**
