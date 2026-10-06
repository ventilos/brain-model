BM-A031 Rev2 – Amendment-002 compatibility record

Project: Brain Model (BM-2026)
Analysis: BM-A031 G2 corrective runner – Revision 2
Date: 2026-10-02
Timestamp of Library update: 2026-10-02T21:13:41+02:00
Status: PROTOCOL_COMPATIBILITY_VERIFIED / CORE_MATH_VERIFIED /
AMENDMENT002_REPORTING_COMPLIANT / CHECKPOINT_V3_CONTRACT_VERIFIED /
FULL_G2_NOT_RUN / G1_UNCHANGED

Scope

This record documents the post-preregistration BM-A031 Revision 2
implementation after the explicit pre-execution Amendment-002 rule for
undefined G2 transition rows. It does not reopen or modify BM-A011 R3 or
G1 and does not report a full G2 scientific result.

Revision lineage

1. Original BM-A031 patched runner SHA-256:
53ea3af023e20b22ce8dbe6c320fa1f57c320854c96e3d29803ce79c6c6d2ff1.
2. Amendment-002-aware intermediate runner SHA-256:
abef8acdbfc6f1f9269ee60f507984b177b219013249bd2a2793d7514de52538.
3. Current BM-A031 Rev2 runner SHA-256:
f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b.
4. Rev2 regression test SHA-256 before repository-path correction:
eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d.
5. Current path-corrected Rev2 regression test SHA-256:
c126618eaa22d2e1587efa3f6c469cf60e8c85563bbdf5f4e262f955cd9178ff.

The original BM-A031 patch note remains historical provenance and must
not be silently rewritten to contain the Rev2 hash. The pre-correction
regression-test hash is likewise retained as historical provenance
rather than overwritten.

Frozen computational semantics implemented by Rev2

• State order: LL, LH, HL, HH.
• Transition rows with zero observed outgoing transitions remain
undefined (NaN computationally; null when serialized as required),
not zero vectors or artificial distributions.
• Null aggregation uses finite defined values only.
• D_self and D_M1 use finite observed/null pairs without
renormalizing the original q_obs weights; an entirely undefined
observed transition row contributes no artificial mismatch.
• D_occ is unaffected by the undefined-transition-row rule.
• N2 run boundaries remain respected; transitions do not cross run
boundaries.
• Checkpoint schema is V3 and records runner SHA-256, state order,
undefined-row policy and the applicable Amendment-002 identifier.
• Incompatible checkpoint contracts fail closed.

Rev2 reporting correction

Rev2 adds explicit Amendment-002 reporting for undefined transition
rows, including observed undefined-row count/frequency, affected
recording × variant status, and null-ensemble availability. This closes
the reporting-compliance gap detected during the independent audit of
the preceding runner revision.

Regression verification

The Rev2 regression suite was designed to test:

• state-order lock;
• zero-outgoing-row → undefined semantics;
• finite-only null aggregation and no artificial D_self/D_M1
mismatch;
• Amendment-002 and runner SHA in the checkpoint contract;
• fail-closed behavior on incompatible checkpoint contracts;
• absence of stale A030/schema-2 execution labels;
• explicit undefined-row reporting;
• repository-relative runner resolution for a clean clone.

Prepared Rev2 suite result: 7/7 PASS. This result predates the
repository-path-only correction and is retained as historical
verification of the unchanged test logic. It does not independently
certify execution of the current GitHub commit and does not constitute a
full G2 execution.

Repository-path correction – 2026-10-03

The regression-test runner reference was corrected from:

archive/provenance/BM-A031/BM-A031_G2_PATCHED_RUNNER.py

to the canonical repository path:

archive/provenance/BM-A031_G2_PATCHED_RUNNER.py

Only the RUNNER path declaration in
tests/test_bm_a031_amendment002_rev2.py changed. Regression-test
logic, frozen Amendment-002 semantics, and the BM-A031 Rev2 runner were
not changed.

The previous regression-test SHA-256 is retained as historical
provenance:

eaf355239ba8c5920a19e550b3e765b52c0cbe3effd3e737f1c1fe028c3c969d

The current path-corrected regression-test SHA-256 is:

c126618eaa22d2e1587efa3f6c469cf60e8c85563bbdf5f4e262f955cd9178ff

The BM-A031 Rev2 runner SHA-256 remains:

f1619b28939b6a68c812ca8cc9cd4ec7e00eb4aaff9924cc99b061e5da005d7b

Classification:

PATH-ONLY CHANGE / TEST LOGIC UNCHANGED / AMENDMENT-002 SEMANTICS UNCHANGED

The repository commit/push containing the path correction and
corresponding CHANGELOG update was subsequently verified with main and
origin/main aligned at commit a6a6d01.

Methodological caveat retained

For D_M1, finite observed/null cell pairs are used when only part of a
null-median row is undefined. This follows the frozen finite-pair rule
of Amendment-002, but such a partial row is not itself a complete
normalized probability distribution. No post-freeze change to this rule
is introduced here.

Scientific lock

• BM-A011 R3 remains frozen.
• G1 remains closed.
• Full G2 has not been run under BM-A031 Rev2.
• No new G2 scientific result is asserted by this record.
• No mechanism, treatment, absence-of-memory, or generalized Brain
Model claim follows from this implementation update.

Correction – 2026-10-06

The statement above that main and origin/main were aligned “at commit
a6a6d01” cannot be verified: no object with that abbreviated hash exists
in the repository history (all reachable and unreachable objects of the
2026-10-05 working copy were checked). The repository-path correction
and the corresponding CHANGELOG update are contained in commit 5d0fbb4
(2026-10-03T17:14:21+02:00); this record was first committed in c40b814
(2026-10-03T19:48:30+02:00). The original sentence is kept unchanged as
provenance; no other statement of this record is affected.

Since 2026-10-03 the regression test targets the canonical runner
src/BM-A031_G2_PATCHED_RUNNER.py (test SHA-256
1a11a9dc346f350455a89cb6cea664fdf9bde70d7744e40e90c40cb77df701a2;
runner unchanged). The test hashes recorded above are historical.

Change log

• 2026-10-02T21:13:41+02:00 – Added BM-A031 Rev2 compatibility
record; recorded Rev2 runner/test hashes, Amendment-002
computational semantics, corrected reporting compliance, checkpoint
V3 provenance, retained methodological caveat, and unchanged
G1/full-G2 status.
• 2026-10-03 – Repository-path correction incorporated into the
compatibility record. Preserved the pre-correction test hash as
historical provenance and recorded the current path-corrected test
hash. No runner code, regression-test logic, frozen Amendment-002
semantics, G1 status, or full-G2 status changed.
• 2026-10-06 – Correction note added: the commit reference a6a6d01
does not exist in the repository history; the path correction is in
5d0fbb4. Current canonical test identity noted. Record otherwise
unchanged.