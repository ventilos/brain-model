# BM-A027-AMENDMENT-002 — G2 undefined-transition-row policy

**Project:** Brain Model (BM-2026)  
**Parent preregistration:** BM_31 / BM-A027 / BM-CHALLENGE-001 v1.0  
**Prior amendment:** BM-A027-AMENDMENT-001 **Timestamp:** 2026-10-02T18:50:00+02:00 (Europe/Warsaw)
**Applies to:** G2 lower-order diagnostics  
**Status:** `PRE_EXECUTION_METHOD_AMENDMENT / FULL_G2_NOT_RUN / G1_UNCHANGED`

## 1. Reason for amendment

The frozen BM-A027 preregistration defines the G2 lower-order diagnostics:

- `D_occ`
- `D_self`
- `D_M1`
- `z_T`

but does not explicitly specify how a first-order transition-probability row is represented when a K4 state has zero observed outgoing transitions on the valid run-local support.

This implementation choice must therefore be fixed explicitly before full G2 execution.

This amendment does not modify BM-A011 R3, its surrogate ensemble, G0, G1, the locked G1 result, or any R3 p-value.

## 2. Frozen K4 state order

For G2 matrices and vectors the symbolic state order is fixed as:

`LL, LH, HL, HH`

All occupancy vectors, transition matrices, serialized outputs, diagnostic labels and downstream summaries must use this order.

State labels must not be inferred from an alternative display order.

## 3. Undefined transition-row definition

For state `i`, let

`N_i = sum_j C_ij`

where `C_ij` is the number of valid run-local transitions from state `i` to state `j`.

If:

`N_i > 0`

then:

`P(j|i) = C_ij / N_i`.

If:

`N_i = 0`

the transition distribution conditional on state `i` is not empirically defined.

The corresponding complete row of `P` is therefore represented as undefined (`NaN` in computation; `null` where required for JSON serialization).

An undefined row must not be replaced by a vector of zeros or by an artificial probability distribution.

## 4. Null-ensemble aggregation

For every transition-matrix cell, the null reference is calculated from finite defined surrogate values only.

Thus:

`median_b P_null,b(j|i)`

means the median over surrogate replicates for which the relevant conditional transition probability is defined.

Undefined surrogate values do not enter the median as zeros.

If no finite surrogate value exists for a required cell, its null reference remains undefined.

## 5. D_self policy

The preregistered quantity is:

`D_self = sum_i q_obs(i) * |P_obs(i,i) - median_b P_null,b(i,i)|`.

Under this amendment, a contribution is evaluated only when both the observed self-transition probability and its null reference are defined.

Undefined terms contribute no artificial discrepancy.

Equivalently, computation is restricted to finite observed/null pairs while retaining the preregistered occupancy weighting `q_obs(i)` for evaluated states.

No renormalization of the remaining occupancy weights is introduced.

## 6. D_M1 policy

The preregistered quantity is:

`D_M1 = sum_i q_obs(i) * 0.5 * sum_j |P_obs(j|i) - median_b P_null,b(j|i)|`.

For a state with no observed outgoing transitions, the conditional transition distribution is undefined and that row is not treated as a zero-probability distribution.

For each state row, discrepancy is calculated only over defined observed/null cell pairs.

If an observed row contains no defined transition probabilities, its row discrepancy contributes zero rather than an artificial total-variation distance.

No redistribution or renormalization of `q_obs(i)` is performed.

## 7. Occupancy diagnostic

`D_occ` is unaffected by the undefined-transition-row policy because occupancy probabilities remain defined independently of outgoing-transition availability.

Its preregistered definition remains unchanged.

## 8. z_T

The preregistered `z_T` definition remains unchanged.

If the surrogate null standard deviation is numerically zero, the BM-A027 requirement to use the exact finite-ensemble rank percentile instead of inventing a z-score remains binding.

## 9. Run boundaries

Transition counts remain restricted to the frozen valid support.

Transitions must never cross contiguous N2-run boundaries.

This amendment does not change the R3 support definition.

## 10. Implementation and checkpoint consequences

The BM-A031 candidate implementation adopts the policy specified above.

Because this policy changes the interpretation of transition matrices relative to implementations that encoded undefined rows as zeros, checkpoints produced under an earlier incompatible transition-row policy must not be silently reused for the amended full G2 execution.

The amended implementation must use a checkpoint contract that records at minimum:

- checkpoint schema version;
- runner SHA-256;
- K4 state order;
- undefined-transition-row policy;
- applicable BM-A027 amendment identifier.

Incompatible checkpoints must be rejected or quarantined rather than automatically resumed.

## 11. Reporting requirement

G2 outputs must explicitly report:

- state order;
- undefined-row policy;
- number/frequency of undefined observed rows;
- corresponding undefined/null-ensemble availability where relevant;
- whether any recording×variant diagnostic was affected by undefined rows.

The policy must be disclosed in the G2 execution record and final methodological report.

## 12. Inferential status

This amendment resolves an implementation ambiguity in the G2 diagnostic layer.

It does not:

- change the locked BM-A011 R3 result;
- reopen G1;
- alter any R3 empirical p-value;
- convert G2 into a new hypothesis test;
- create a post-hoc threshold for overturning G1;
- establish higher-order specificity;
- establish a biological memory mechanism.

G2 remains mandatory diagnostic context under the operative BM-A027 framework.

## 13. Relationship to BM-A031

BM-A031 was prepared before this ambiguity was formally resolved and therefore previously carried:

`PROTOCOL_COMPATIBILITY_PENDING`.

After this amendment is frozen, BM-A031 may be evaluated against the amendment.

Only after successful code-level verification of exact compliance may its protocol status be promoted to:

`PROTOCOL_COMPATIBILITY_VERIFIED`.

That promotion does not imply that full G2 has been executed.

## 14. Freeze rule

This amendment must be committed and frozen before inspection of any full-G2 result produced using this policy.

Once frozen, the undefined-transition-row policy must not be changed in response to the resulting G2 effect sizes, correlations, confidence intervals or other outcomes.

Any subsequent change requires a separately versioned amendment and must preserve the complete provenance chain.

## 15. Change log

2026-10-02T18:50:00+02:00 | BM-A027-AMENDMENT-002 | explicit pre-full-G2 policy for transition rows with zero outgoing transitions; K4 state order LL,LH,HL,HH fixed; undefined rows represented as NaN/null; finite-only null aggregation; no artificial zero-row discrepancy; incompatible checkpoints not reused; BM-A011 R3 and G1 unchanged | PRE_EXECUTION_METHOD_AMENDMENT / FULL_G2_NOT_RUN / G1_UNCHANGED`