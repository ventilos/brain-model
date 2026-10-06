# BM-CI-CERT-001 v0.2 — delivery record

The three files in this folder are the unchanged delivery record of the BM-CI-CERT-001 v0.2 certification patch (2026-10-05). They were moved here from the repository root on 2026-10-06; their bytes are unchanged.

| File | SHA-256 |
|—|—|
| `BM-CI-CERT-001_V0.2_REPORT_2026-10-05.md` | `a29e3bbf70025b1fc83e955b46a9e5bfa45663aea1028679e59d4bbda0498bbe` |
| `CHANGELOG_APPEND.md` (merged into `CHANGELOG.md`, entry 2026-10-05) | `5e9c77c47cc9208dfa2fc4bb3b6f7ac45024c6b2f76a8f1bd082bdeb2c699384` |
| `PACKAGE_FILE_SHA256.txt` | `68925178dea40f6dbd56e4cecbd50577658ea7f41ac427623c3598ab74c0b3e1` |

Paths inside `PACKAGE_FILE_SHA256.txt` are relative to the repository root as it was at commit `5ed4edb`. To re-check them:

```bash
git checkout 5ed4edb
sha256sum -c PACKAGE_FILE_SHA256.txt
```

The active contract files stay in place and are unchanged: `tools/verify_ci_contract.py`, `.github/workflows/ci-cert.yml`, `requirements-ci.txt` and `CONTRACT_SHA256.txt`.

Scope reminder: `CI_CONTRACT_PASS` certifies the frozen BM-A031 Rev2 contract only. It is not `FULL_PROJECT_REPRODUCIBILITY_PASS`; full G2 remains `NOT_RUN` and G1 remains `UNCHANGED`.
