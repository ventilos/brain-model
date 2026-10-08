# BM-2026 historical G0/R3 provenance import

Date: 2026-10-08. Scope: recovered original artifacts only.

Copy the `archive/` directory into the existing repository root, preserving paths.
Do NOT overwrite existing files with the same names unless their content has been compared.
The historical files do not change the frozen BM-A028 decision, BM-A031 Rev2,
CI, preregistration, or the scientific interpretation.

Status: G0 PASS; G1 FAIL; G2/G3 NOT_RUN.
G1 claim: RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS.

The ZIP contains nested original ZIP archives. Preserve them byte-for-byte.
Check MANIFEST_SHA256.json before importing; compare destination paths to existing
repository files before staging any changes. This package is not a Git commit.
