## 2026-10-05 — BM-CI-CERT-001 v0.2

- Added fail-closed CI contract verification for frozen BM-A031 Rev2.
- Added runtime verification of Python 3.13.5 and frozen package versions.
- Added integrity checks for requirements-ci.txt and ci-cert.yml.
- Strengthened negative integrity self-test to require rejection by the production hash verifier.
- Preserved scientific boundary: FULL_G2_NOT_RUN; G1_UNCHANGED.
- CI_CONTRACT_PASS must not be reported as FULL_PROJECT_REPRODUCIBILITY_PASS.
- Remote status remains NOT YET VERIFIED until GitHub Actions completes successfully on current main.