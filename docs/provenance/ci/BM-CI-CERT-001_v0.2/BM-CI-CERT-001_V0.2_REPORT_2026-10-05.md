# BM-CI-CERT-001 v0.2 — certification patch record

Date: 2026-10-05
Status before remote execution: **LOCAL CI CONTRACT PASS / REMOTE NOT YET VERIFIED**

## Scope
This patch certifies only the frozen BM-A031 Rev2 CI contract. It does **not** certify full-project reproducibility and does not execute FULL_G2.

## Frozen controls
- Python: 3.13.5
- numpy: 2.3.5
- pandas: 2.2.3
- scipy: 1.17.0
- pytest: 9.0.2
- canonical BM-A031 runner SHA-256: f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b
- BM-A031 Rev2 regression test SHA-256: 1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2
- requirements-ci.txt SHA-256: 2905ba50505ca0a4dd03ae415e4e8e84dedb4d4ef560fa8e051e4306aa681553
- ci-cert.yml SHA-256: a6c8644c417419fcfba2a5d155f992f5944fbebcf087e59db224a2b9dc80c968

## v0.2 corrections after five-path audit
1. Negative integrity test invokes the same hash-verification function and requires rejection of a deliberately mutated runner.
2. Python 3.13.5 is verified at runtime, not merely requested by the workflow.
3. requirements-ci.txt and ci-cert.yml are included in the frozen hash contract.
4. CI contract PASS is explicitly separated from full-project reproducibility.
5. FULL_G2 remains NOT_RUN and G1 remains UNCHANGED.

## Reproducibility boundary
The supplied current project snapshot does not contain the historical BM-PKG-002 utilities verify_library.py, verify_claims.py, compare_golden.py or reproduce.py. They are therefore not reconstructed or silently imported from another project state. Full-project reproducibility remains NOT_TESTED.
