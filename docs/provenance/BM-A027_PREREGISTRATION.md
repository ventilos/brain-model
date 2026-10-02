BM_31 — BM-CHALLENGE-001: post-R3 specificity + value-added gate (BM-A027)

Project: Brain Model (BM-2026)
Analysis ID: BM-A027 / BM-CHALLENGE-001
Timestamp freeze: 2026-09-29T21:54:05+02:00 (Europe/Warsaw)
Authority at freeze: BM_00 v41
Status: FROZEN_PREREGISTRATION / EXECUTION_AFTER_R3 / R3_UNCHANGED / NO_CLAIM_PROMOTION

0. Purpose and freeze rule

This document freezes the next inferential step before the final cohort-level result of BM-A011 R3 is available. It does not modify the currently running BM-A011 scientific package, its nulls, its decision rules, or any completed BM-A004–BM-A008 result.

The central question is:

> **Does the temporal/network signal attributed to Brain Model contain reproducible information beyond what is explainable by preserved temporal/spectral nuisance, lower-order state structure, and simpler predictive models?**

Freeze rule: once the final BM-A011 cohort summary becomes available, the hypotheses, primary endpoints, gates, comparator families, direction of tests, and status mapping below may not be changed in BM-A027 v1.0. Any later change requires a separately versioned amendment (BM-A027-AMENDMENT-*) and must be labeled sensitivity/exploratory rather than confirmatory.

1. Snapshot at freeze

1.1 Current authoritative project state

• Current project header: BM_00 v41.
• Frozen raw-signal package: BM-A011-ST44-RAW-NULL-V3CS-R3.
• Current execution launcher: BM-A024.
• BM-A011 scientific package SHA-256: 9ab675e3acd157b21845f5f242b43274337c6cb4f5121efc59ad03a84110414f.
• Frozen production contract: 38 recordings / 19 participants; pilot subjects {21,22,24} excluded; B=1999; seed=20260921; meta_draws=100000; statistic T_cs; three null variants common_phase_run, independent_channel_phase, epochwise_common_phase.

1.2 Directly observed execution snapshot

At 2026-09-29T21:54:05+02:00 the current Drive tree shows:

• 27/38 COMPLETE: ST7011–ST7151 over the locked hold-out sequence, excluding pilot IDs;
• 1/38 PARTIAL: ST7152, with OBSERVED_EPOCH_METRICS.csv present but no complete three-variant summary/provenance bundle yet;
• 10/38 NOT STARTED: ST7161, ST7162, ST7171, ST7172, ST7181, ST7182, ST7191, ST7192, ST7201, ST7202;
• final cohort aggregation is not yet treated as available.

This snapshot is execution metadata only and carries no scientific interpretation.

2. Source-derived constraints already fixed before BM-A027

The following are inherited constraints, not new choices made after looking at R3 outcomes.

2.1 Common-support endpoint

The corrected primary state statistic compares M2 and M1 on the same target support:

T_cs = 2[ll(M2; C) - ll(M1; C)]

with intensive endpoints derived from the same common support, including CMI_nats and bias-corrected CMI_MM_nats. Legacy T_v2 is retained only as a regression/provenance quantity and is not a valid primary treatment endpoint.

2.2 Already-established constraints from BM-A004–BM-A008

• IN_SAMPLE_CONDITIONAL_DEPENDENCE: DETECTED_BOUNDED on the frozen K4 representation.
• STABLE_OUT_OF_RUN_ORDER2_PREDICTION: NOT_DEMONSTRATED (BM-A007).
• ORDER2_GENERATIVE_MODEL_PREFERENCE: NOT_SUPPORTED_BY_KT_MDL_BAYES (BM-A008).
• legacy temazepam–placebo T_stagecond: SUPERSEDED_NOT_SUPPORTED_BY_CORRECTED_ENDPOINT.
• None of these may be silently upgraded by a positive raw-signal R3 result.

2.3 Existing frozen R3 interpretation rule

All three surrogate variants are reported separately.

• common_phase_run: primary common-spectrum-preserving temporal null.
• epochwise_common_phase: conditional / E_eff-preserving, zero-lag-structure-preserving null for T_cs; it cannot independently validate E_eff.
• independent_channel_phase: sensitivity null because it additionally disrupts cross-channel phase structure.

The original R3 intersection-union decision rule remains binding:

• both common-phase variants with empirical group p < 0.05 → RAW_SIGNAL_COMMON_PHASE_SUPPORTED_BOUNDED;
• both with p >= 0.05 → NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS;
• disagreement → INCONCLUSIVE_NULL_SENSITIVE.

3. BM-CHALLENGE-001 architecture

The challenge has five sequential gates. A later gate cannot repair failure of an earlier hard gate. Passing a gate only licenses the narrow claim explicitly associated with that gate.

────────

G0 — execution integrity gate [HARD]

Required inputs

The existing BM-A011 R3 run only. No recomputation under altered scientific settings is allowed for G0.

PASS criteria

All must hold:

1. 38/38 locked recordings have exact-valid recording checkpoints.
2. Every recording contains all three frozen surrogate variants.
3. Every recording×variant has B=1999 accepted replicates under the frozen package.
4. acceptance_rate >= 0.99 for every recording×variant.
5. seed=20260921, meta_draws=100000, and the frozen code/input provenance match exactly.
6. All required production audit checks in AUDIT_12X.csv pass.
7. Final GROUP_SIGNAL_NULL_SUMMARY.csv and final cohort audit are present and internally consistent.
8. Population inference uses 19 participants as the independent unit and preserves the frozen two-night handling.

FAIL status

Any hard failure → NO_INFERENCE_EXECUTION_FAILURE.

No scientific interpretation of R3 is permitted until G0 passes.

────────

G1 — frozen raw-signal null gate [HARD, ALREADY PRESPECIFIED]

No new threshold is introduced here. Apply the pre-existing R3 rule exactly.

Outcomes

• G1-PASS: both common_phase_run and epochwise_common_phase empirical group p-values <0.05.
• G1-FAIL: both empirical group p-values >=0.05.
• G1-INCONCLUSIVE: one passes and one fails.

independent_channel_phase is reported but cannot by itself determine G1.

Permitted claim after G1-PASS

Only:

> The observed N2-localized common-support temporal statistic is unusual under both prespecified common-phase raw-signal nulls in the locked ST44 hold-out cohort.

Not permitted from G1 alone: stable Markov(2), biological memory mechanism, universal C, C-field ontology, drug effect, consciousness claim, or psychosis mechanism.

────────

G2 — lower-order state-structure diagnostic gate [NEW PREREGISTRATION; POST-R3]

Purpose

Determine whether the raw-null shift in T_cs is tightly coupled to simpler changes in K4 occupancy or first-order transition structure. These diagnostics do not retroactively alter the validity of the frozen G1 p-values; they constrain interpretation.

Data unit

For each of the 38 recordings and each of the three frozen variants, reconstruct the observed K4 sequence and every accepted surrogate K4 sequence using the exact frozen thresholds/operator used in R3.

Fixed diagnostics

For K4 states k=1..4:

1. Occupancy total-variation mismatch

D_occ = 0.5 * sum_k |q_obs(k) - median_b q_null,b(k)|

2. Weighted self-transition mismatch

D_self = sum_k q_obs(k) * |P_obs(k,k) - median_b P_null,b(k,k)|

3. Weighted full first-order transition mismatch

D_M1 = sum_i q_obs(i) * 0.5 * sum_j |P_obs(j|i) - median_b P_null,b(j|i)|

4. Primary R3 standardized shift

z_T = (T_cs_obs - mean_b T_cs_null,b) / sd_b(T_cs_null,b).

If the null standard deviation is numerically zero, use the exact finite-ensemble rank percentile instead of inventing a z-score.

Population diagnostics

For each null variant separately:

• Spearman rho(z_T, D_occ);
• Spearman rho(z_T, D_self);
• Spearman rho(z_T, D_M1).

Participant is the resampling unit. Two nights remain clustered within participant. Uncertainty: participant-cluster bootstrap, B=10000, seed 20260929.

Also report:

• observed and null occupancy vectors by recording;
• observed and null self-transition rates;
• observed and null first-order transition matrices;
• leave-one-participant-out sensitivity of the three correlations.

Interpretation rule

G2 is diagnostic, not a binary validity filter. However a claim of higher-order specificity is blocked if the R3 effect is strongly explained by lower-order mismatch and does not survive G3.

No post-hoc cutoff for “strongly explained” may be invented. The mandatory outputs are effect sizes, bootstrap intervals, scatter/correlation diagnostics and G3 value-added results.

────────

G3 — continuous-domain value-added gate [NEW PREREGISTRATION; HARD FOR STRONGER CLAIM]

Purpose

Test whether the temporal information targeted by BM adds out-of-sample predictive value beyond simpler continuous-domain models, thereby avoiding the invalid inference “symbolic M2 > M1 ⇒ biological second-order memory”.

Outer inferential split

Leave-one-participant-out (LOPO), 19 outer folds. Both nights of the held-out participant remain outside all model fitting, normalization, hyperparameter selection and feature thresholding.

Fixed comparator families

All are evaluated on identical held-out targets/support within a fold.

• C0: static/stage-only baseline (no temporal history beyond stage/context variables needed to define the target).
• C1: regularized AR/VAR(1).
• C2: regularized AR/VAR(2+) with order chosen only inside training data from a fixed candidate grid p ∈ {2,3,4,5}.
• C3: linear Gaussian state-space model (LGSSM), latent dimension chosen only within training data from d ∈ {2,3,4,6,8}.
• C4: switching linear/state-space model, number of regimes chosen only within training data from K ∈ {2,3,4,5,6}.
• BM: multiaxis Brain Model predictor built from the continuous/spectral/information features defined by the frozen BM pipeline; all scaling, thresholds and feature-selection steps are estimated inside the outer training set only.

If a comparator cannot be stably fitted in a fold, that failure is recorded; it may not be silently dropped. A simpler fallback must be specified before inspecting the held-out score for that fold.

Primary score

Mean held-out log predictive density per target/sample on common support.

Secondary descriptive scores: MSE/MAE where defined, but they cannot replace the primary log-score decision.

Comparator for the gate

Within each outer training fold, nested CV selects the strongest non-BM comparator among C0–C4. The held-out participant yields:

Delta_LPD_s = LPD_BM,s - LPD_best-baseline,s.

G3-PASS criterion

Both must hold on the 19 independent participants:

1. mean Delta_LPD > 0;
2. exact two-sided sign-flip test over participant-level Delta_LPD gives p < 0.05.

Report median, IQR and all participant-level differences. Exact enumeration over 2^19 = 524288 sign patterns is used; no Monte Carlo approximation is needed for the primary participant-level test.

If the mean is positive but exact p is >=0.05, or vice versa, G3 = INCONCLUSIVE_VALUE_ADDED.

Important non-upgrade rule

Even G3-PASS does not establish a stable Markov(2) law. It establishes only bounded predictive value of the specified BM representation over the strongest tested simpler comparator on ST44.

────────

G4 — representation robustness gate [NEW PREREGISTRATION]

Purpose

Prevent a claim from depending on one arbitrary graph/spectral implementation.

Fixed sensitivity axes

Where the input permits the comparison without redefining the scientific target:

1. graph density / threshold over a preregistered grid rather than one selected threshold;
2. at least two graph-construction variants;
3. signed versus explicitly transformed unsigned handling, where mathematically defined;
4. lambda_2 alone versus (lambda_2, S_spec) versus a fuller spectral profile;
5. static occupancy/spectrum versus trajectory features.

The exact numeric threshold grid must be frozen in the executable configuration before G4 computation and may not be selected from outcome plots.

G4 interpretation

A stronger representation-level claim requires the sign/direction of the primary value-added effect to be stable across the predefined multiverse and not confined to a single threshold or graph construction.

No single lambda_2 result may be promoted to a universal order parameter.

────────

G5 — external replication gate [REQUIRED FOR GENERALIZATION]

ST44 cannot by itself establish a general Brain Model law. Any promotion beyond ST44_BOUNDED requires replication on a genuinely independent context/dataset with:

• frozen preprocessing/operator definition;
• identical or explicitly mapped estimand;
• independent participants;
• no retuning of decision thresholds using ST44 outcomes;
• the same direction of the preregistered primary effect;
• subject-level inference.

Failure of external replication leaves any positive ST44 result as dataset-bounded.

4. Final claim-state mapping

Apply the first applicable state after all required inputs are available:

1. G0 fails → NO_INFERENCE_EXECUTION_FAILURE.
2. G0 pass + G1 fail → RAW_SIGNAL_NOT_SUPPORTED_UNDER_PRESPECIFIED_COMMON_PHASE_NULLS; state-level in-sample dependence remains a bounded descriptive result only.
3. G1 inconclusive → RAW_SIGNAL_INCONCLUSIVE_NULL_SENSITIVE; no higher-order-specific promotion.
4. G1 pass, G3 not passed → RAW_SIGNAL_NULL_DEVIATION_SUPPORTED_BOUNDED; higher-order/mechanistic/value-added claim blocked.
5. G1 pass + G3 pass, but G4 unstable → VALUE_ADDED_SUPPORTED_IMPLEMENTATION_SENSITIVE; no representation-general claim.
6. G1 pass + G3 pass + G4 robust → MULTIAXIS_TEMPORAL_VALUE_ADDED_SUPPORTED_ST44_BOUNDED.
7. State 6 + independent G5 replication → eligible for a separately reviewed cross-dataset claim; no automatic promotion is performed by BM-A027 itself.

5. Explicitly excluded claim classes

BM-CHALLENGE-001 cannot, regardless of outcome, establish:

• a universal scalar C;
• a biological or ontological C-field;
• consciousness from one graph/spectral statistic;
• a stable Markov(2) generative law unless separately supported against BM-A007/BM-A008 constraints;
• causal neuronal memory from symbolic state dependence;
• a temazepam/placebo treatment effect;
• clinical psychosis hysteresis;
• a causal mechanism from an observational/null-deviation result.

6. Output contract

Post-R3 execution of BM-A027 must create, at minimum:

• BM-A027_PREREGISTRATION_LOCK.md
• BM-A027_FROZEN_CONFIG.json
• BM-A027_R3_FINAL_SNAPSHOT.json
• BM-A027_LOWER_ORDER_DIAGNOSTICS.csv
• BM-A027_LOWER_ORDER_SUMMARY.json
• BM-A027_CONTINUOUS_MODEL_ZOO_RESULTS.csv
• BM-A027_PARTICIPANT_VALUE_ADDED.csv
• BM-A027_REPRESENTATION_MULTIVERSE.csv
• BM-A027_CLAIM_GATE.json
• BM-A027_FINAL_REPORT.md
• MANIFEST.csv
• SHA256SUMS

Every final report must preserve the distinction between:

• raw-signal null deviation;
• lower-order mismatch;
• predictive value added;
• representation robustness;
• external replication.

7. Execution order

1. Do not alter BM-A011/BM-A024. Allow the frozen R3 run to finish unchanged.
2. Verify 38/38 checkpoints and final aggregation → G0.
3. Apply the already frozen G1 decision rule without reinterpretation.
4. Run G2 lower-order diagnostics on the completed frozen surrogate ensemble.
5. Implement and independently audit the G3 continuous-domain model zoo before fitting held-out folds.
6. Freeze G4 numeric multiverse grid before running G4.
7. Generate claim gate and final report.
8. External G5 replication is a later, separately versioned experiment.

8. Separation of source-derived constraints from new preregistration choices

Source-derived / previously frozen

• 38 recordings / 19 participants; pilot exclusions {21,22,24}.
• B=1999, seed 20260921, meta-null 100000.
• the three R3 surrogate variants and T_cs.
• R3 common-phase intersection-union rule.
• participant as population unit.
• BM-A007: no demonstrated stable out-of-run M2 advantage.
• BM-A008: no M2 generative preference under KT/MDL/Bayes.
• post-R3 requirement for occupancy/self-transition diagnostics.
• no mid-run scientific modification of R3.

New BM-A027 preregistration choices

• explicit five-gate challenge architecture G0–G5;
• exact lower-order diagnostic definitions D_occ, D_self, D_M1;
• participant-cluster bootstrap B=10000, seed 20260929 for G2 uncertainty;
• LOPO continuous-domain model-zoo test;
• exact participant-level sign-flip criterion for value added;
• final claim-state mapping;
• requirement to freeze a graph/spectral multiverse before G4 execution.

9. Change log

2026-09-29T21:54:05+02:00 | BM-A027 / BM_31 / BM-CHALLENGE-001 | frozen post-R3 preregistration: G0 execution integrity, G1 inherited raw-null rule, G2 lower-order diagnostics, G3 continuous-domain value-added, G4 representation robustness, G5 external replication; current R3 untouched | FROZEN_PREREGISTRATION / R3_UNCHANGED / NO_CLAIM_PROMOTION

10. Freeze statement

BM-A027 v1.0 is frozen before inspection of the final BM-A011 cohort-level R3 outcome. The currently observed per-recording execution state is recorded only to establish timing and provenance. No final group result was used to select the gates or their decision thresholds.

KONIEC BM_31 — BM-A027 / BM-CHALLENGE-001