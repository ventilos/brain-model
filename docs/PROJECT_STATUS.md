# Brain Model — Project Status

**Project:** Brain Model (BM-2026)  
**Repository:** brain-model  
**Status:** ACTIVE DEVELOPMENT  
**Canonical branch:** main

## Purpose

This file is the canonical entry point for the current state of the Brain Model project.

It distinguishes the current project state from historical analyses, superseded implementations, audit artifacts, generated results, and external/raw data.

## Repository principles

1. The repository must remain reproducible and auditable.
2. Current source code must be separated from historical and superseded artifacts.
3. Raw datasets must not be committed to the repository unless explicitly approved.
4. Generated results must be distinguishable from source inputs.
5. Scientific claims must remain traceable to their source analysis and implementation.
6. Historical artifacts are preserved for provenance but do not automatically define the current implementation.
7. Changes to the canonical implementation must be recorded in CHANGELOG.md and Git history.

## Current repository bootstrap

The repository currently contains the initial Git infrastructure:

- README.md
- CHANGELOG.md
- .gitignore
- docs/PROJECT_STATUS.md

The scientific implementation, tests, reproducibility infrastructure, provenance records, and validated project artifacts will be migrated incrementally.

## Migration policy

Each imported Brain Model artifact will be classified before inclusion as one of:

- CURRENT
- SOURCE
- TEST
- CONFIG
- GENERATED
- PROVENANCE
- SUPERSEDED
- EXTERNAL/RAW

No historical package will be copied wholesale into the canonical source tree without classification.

## Reproducibility baseline

The existing Brain Model audit packages provide the historical reproducibility baseline.

Their manifests, checksums, verification scripts, reference outputs, and provenance records will be migrated or referenced without silently changing their scientific meaning.

## Current phase

Repository bootstrap and controlled migration.

The next phase is creation of the canonical repository structure followed by artifact-by-artifact migration of the latest validated Brain Model state.