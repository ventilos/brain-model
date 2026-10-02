BM-A027-AMENDMENT-001 — pre-outcome source-consistency correction

Project: Brain Model (BM-2026)
Parent preregistration: BM_31 / BM-A027 / BM-CHALLENGE-001 v1.0
Timestamp: 2026-09-29T22:01:01+02:00 (Europe/Warsaw)
Status: FROZEN_AMENDMENT / PRE_FINAL_R3 / R3_UNCHANGED / NO_CLAIM_PROMOTION

Reason for amendment

After the v1.0 freeze, a project-source consistency check confirmed an earlier roadmap constraint: S_spec_norm is Candidate #1, not frozen, while lambda_2 is a lower-priority sensitivity. Therefore v1.0 must not imply that a frozen spectral BM predictor already exists. This amendment is made before use of any final cohort-level BM-A011 R3 result. The original v1.0 remains archived and immutable as provenance.

No scientific setting of BM-A011/BM-A024 is changed.

A1 — replacement of G3 model-family definition

Replace the v1.0 G3 definition BM versus strongest non-BM comparator with the following source-consistent test.

G3 — continuous-domain temporal value-added gate

Target domain: the continuous variables already produced by the frozen ST44 operator before K4 thresholding, primarily the continuous (E_eff, ILMI) representation on the same valid/common support. No new S_spec_norm, lambda_2, K16, graph-density, or phase-synchrony axis may enter the G3 primary test.

Outer split: leave-one-participant-out, 19 folds; both nights of the held-out participant remain outside normalization, parameter fitting, hyperparameter selection and threshold estimation.

Simple family S:

• S0: static/stage-only baseline;
• S1: regularized VAR(1) / first-order continuous temporal baseline.

Richer temporal family R:

• R2: regularized VAR(p), p ∈ {2,3,4,5} selected within training data only;
• R3: LGSSM, latent dimension d ∈ {2,3,4,6,8} selected within training data only;
• R4: switching linear/state-space model, regimes K ∈ {2,3,4,5,6} selected within training data only.

Within each outer training fold, nested CV chooses the strongest model in family S and the strongest model in family R. The held-out participant yields

Delta_LPD_s = LPD_best-R,s - LPD_best-S,s.

Primary score: mean held-out log predictive density per target/sample on identical support.

G3-PASS:

1. mean Delta_LPD > 0, and
2. exact two-sided sign-flip test across 19 participant-level differences gives p < 0.05.

The exact sign-flip enumeration has 2^19 = 524288 sign patterns.

G3-INCONCLUSIVE: only one of the two PASS requirements is met.

G3-FAIL: neither requirement is met or mean Delta_LPD <= 0 with no significant positive advantage.

Interpretation

G3-PASS supports only:

CONTINUOUS_TEMPORAL_VALUE_ADDED_ST44_BOUNDED

It does not identify Markov order 2, a biological memory mechanism, a C-field ontology, or a new frozen BM axis.

A2 — G4 is separated from the primary ST44 challenge

The representation/spectral multiverse in v1.0 is reclassified as secondary / future representation-development work and is not part of the primary G0–G3 decision chain for ST44.

Current source-derived status is fixed as:

• S_spec_norm: Candidate #1, not frozen; required gate = incremental distinctness + cross-night reliability + held-out/raw-null evaluation.
• lambda_2: lower-priority sensitivity/control; not a primary axis.
• frequency-domain synchrony/phase coupling: backup candidate requiring a separately frozen estimator/band and artifact controls.
• LZC: external reference; not to be consumed as a K16 coordinate.
• transition/Hamming/hotspot/cascade metrics: outcomes/diagnostics; not K16-defining bits.

Any future spectral/K16 analysis requires a separately frozen analysis ID and cannot be chosen after inspecting its own outcome to rescue G3.

A3 — operative primary claim mapping

The operative BM-CHALLENGE-001 primary chain is now:

1. G0 fail → NO_INFERENCE_EXECUTION_FAILURE.
2. G0 pass + G1 fail → RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS.
3. G1 inconclusive → RAW_SIGNAL_INCONCLUSIVE_NULL_SENSITIVE.
4. G1 pass + G3 fail/inconclusive → RAW_SIGNAL_NULL_DEVIATION_SUPPORTED_BOUNDED; stronger temporal-specific claim blocked.
5. G1 pass + G3 pass → CONTINUOUS_TEMPORAL_VALUE_ADDED_ST44_BOUNDED.
6. Cross-dataset/general claim still requires an independent replication gate and a separate review.

G2 remains mandatory diagnostic context between G1 and final interpretation, but no unregistered post-hoc G2 cutoff can overturn the frozen G1 p-value.

Change log

2026-09-29T22:01:01+02:00 | BM-A027-AMENDMENT-001 | pre-outcome source-consistency correction: removed implication of a frozen spectral BM predictor; G3 redefined as rich-vs-simple continuous temporal model-zoo test using frozen ST44 continuous variables; G4 separated as future representation work; R3 unchanged | FROZEN_AMENDMENT / PRE_FINAL_R3 / NO_CLAIM_PROMOTION

Operative status

BM-A027 v1.0 + this Amendment-001 form the operative preregistration. Where they conflict, Amendment-001 controls. All other v1.0 sections remain unchanged.

KONIEC BM-A027-AMENDMENT-001