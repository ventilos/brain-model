# BM-2026 — G0/R3 historical evidence import closure

**Record ID:** BM-G0R3-IMPORT-CLOSURE-2026-10-08  
**Date:** 2026-10-08  
**Scope:** Documentation-only provenance closure; no scientific rerun or claim promotion.  
**Status:** USER-REPORTED IMPORT / COMMIT / CI GREEN / REGRESSION PASS; commit SHA and workflow run IDs not independently captured in this record.

## Provenance and frozen scientific decision

The four source artifacts below were recovered and verified byte-for-byte against the listed SHA-256 digests before the import package was built. They were staged for the repository under `archive/provenance/g0_r3/` and the user subsequently reported a successful GitHub commit, green GitHub Actions, and a passing regression test. This document does not independently establish the GitHub tree SHA, commit SHA, or the CI logs.

BM-A028 frozen status: **G0 PASS; G1 FAIL; G2 NOT_RUN; G3 NOT_RUN**. The G1 claim state remains `RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS`. No G2/G3 completion is implied by a green CI run.

## Source file checksums

| Repository path | Bytes | SHA-256 |
|---|---:|---|
| `archive/provenance/g0_r3/BM-A028_G0_G1_DECISION.json` | 713 | `e37c36d089afd09ede83b1949b367552fa1d03c00530f4c0a5680deef17acde2` |
| `archive/provenance/g0_r3/BM-A028_G0_G1_DECISION.md` | 481 | `39c73abcbee30408b677e5337aae015fc6222a5e77cc60657916f56dd78292c4` |
| `archive/provenance/g0_r3/BM-A011_RAW_NULL_V3CS_R3_B1999.zip` | 7389894 | `20b6e95d482c3371ce5b95ee44f861b6f39f327dbbd61d40fe276e674c6726f3` |
| `archive/provenance/g0_r3/BM-A011_STEP3_FULL_RAW_SIGNAL_V3CS_R3_2026-09-26.zip` | 32525 | `9ab675e3acd157b21845f5f242b43274337c6cb4f5121efc59ad03a84110414f` |

## Evidence classification

- **Verified locally:** presence, file sizes, SHA-256 of all four originals; integrity of both nested ZIP archives.
- **Reported by repository operator:** transfer to GitHub, commit success, green GitHub Actions, passing regression test.
- **Not independently verified here:** actual remote commit SHA, Actions run URLs, remote blob digests, current remote tree.

## Release handling

This record is an additive document only. Do not overwrite `docs/MIGRATION_LEDGER.md`, `docs/PROJECT_STATUS.md`, `README.md`, `CONTRACT_SHA256.txt`, or frozen analysis files without a content diff and an explicit separate review. Preserve both original BM-A011 ZIP archives byte-for-byte. This record is not itself a release approval.

## Changelog

2026-10-08 — Appended a documentation-only closure record for historical G0/R3 provenance import. Scientific and CI status remain logically distinct.
