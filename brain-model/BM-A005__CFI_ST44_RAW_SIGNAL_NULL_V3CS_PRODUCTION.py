#!/usr/bin/env python3
"""Brain Model BM-A005 — production raw-signal ST44 common-support surrogate null.

This orchestrator wraps the audited BM-A004 common-support operator and makes the
Step-3 production contract fail-closed and Drive-first:
  * raw EDFs are read from an already verified local/Drive mirror, never downloaded;
  * ST44_DOWNLOAD_RECEIPT.csv is the source inventory/condition map;
  * checkpoints are reusable only when code, inputs and all run parameters match;
  * primary statistic names are explicitly T_cs, not legacy T_N2;
  * group output is schema-validated, not merely existence-checked.

Confirmatory scope: locked 19-subject / 38-recording holdout excluding subjects
21, 22 and 24. This remains a retrospective/falsification analysis.
"""
from __future__ import annotations

import argparse, gc, hashlib, importlib.util, json, math, os, shutil, sys, zipfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from scipy import stats

ANALYSIS_ID = "BM-A005-ST44-RAW-NULL-V3CS"
PILOT_SUBJECTS = {21, 22, 24}
DEFAULT_VARIANTS = ["common_phase_run", "independent_channel_phase", "epochwise_common_phase"]
EXPECTED_ST7022_T_V2 = 146.4779585335193
TZ = ZoneInfo("Europe/Warsaw")


def now_iso():
    return datetime.now(TZ).isoformat(timespec="seconds")


def hash_file(path: Path, algo="sha256", chunk=8 * 1024 * 1024):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_base(path: Path):
    spec = importlib.util.spec_from_file_location("bm_a004_raw_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import base runner: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def receipt_inventory(receipt: Path, raw_dir: Path, recordings=None, holdout_only=True):
    r = pd.read_csv(receipt)
    req = {"recording", "subject_orig", "condition", "kind", "file", "sha1_expected", "sha1_actual", "bytes", "status"}
    miss = req - set(r.columns)
    if miss:
        raise RuntimeError(f"Receipt missing columns: {sorted(miss)}")
    r = r.copy()
    r["recording"] = r["recording"].astype(str)
    r["condition"] = r["condition"].astype(str)
    r["kind"] = r["kind"].astype(str)
    r["file"] = r["file"].astype(str)
    r["subject_orig"] = r["subject_orig"].astype(int)
    if recordings:
        wanted = set(recordings)
        r = r[r.recording.isin(wanted)].copy()
        missing = wanted - set(r.recording)
        if missing:
            raise RuntimeError(f"Requested recordings absent from receipt: {sorted(missing)}")
    if holdout_only:
        r = r[~r.subject_orig.isin(PILOT_SUBJECTS)].copy()
    if not (r.status.astype(str).str.lower() == "downloaded").all():
        raise RuntimeError("Receipt contains non-downloaded entries")
    if not (r.sha1_expected.astype(str).str.lower() == r.sha1_actual.astype(str).str.lower()).all():
        raise RuntimeError("Receipt expected/actual SHA1 mismatch")
    rows = []
    for rec, g in r.groupby("recording", sort=True):
        if len(g) != 2 or set(g.kind) != {"PSG", "Hypnogram"}:
            raise RuntimeError(f"{rec}: expected exactly PSG + Hypnogram, got {g.kind.tolist()}")
        p = g.set_index("kind")
        subject = int(g.subject_orig.iloc[0])
        condition = str(g.condition.iloc[0])
        if g.subject_orig.nunique() != 1 or g.condition.nunique() != 1:
            raise RuntimeError(f"{rec}: inconsistent subject/condition in receipt")
        psg_name = str(p.loc["PSG", "file"])
        hyp_name = str(p.loc["Hypnogram", "file"])
        psg = raw_dir / psg_name
        hyp = raw_dir / hyp_name
        for kind, fp in [("PSG", psg), ("Hypnogram", hyp)]:
            rr = p.loc[kind]
            if not fp.exists():
                raise FileNotFoundError(fp)
            if fp.stat().st_size != int(rr["bytes"]):
                raise RuntimeError(f"{fp.name}: size mismatch {fp.stat().st_size} != {int(rr['bytes'])}")
            got = hash_file(fp, "sha1")
            if got.lower() != str(rr["sha1_expected"]).lower():
                raise RuntimeError(f"{fp.name}: SHA1 mismatch {got} != {rr['sha1_expected']}")
        rows.append({
            "recording": rec,
            "subject": subject,
            "night": int(rec[-1]),
            "condition": condition,
            "psg": str(psg),
            "hypnogram": str(hyp),
            "psg_sha1": str(p.loc["PSG", "sha1_expected"]).lower(),
            "hyp_sha1": str(p.loc["Hypnogram", "sha1_expected"]).lower(),
            "psg_bytes": int(p.loc["PSG", "bytes"]),
            "hyp_bytes": int(p.loc["Hypnogram", "bytes"]),
        })
    out = pd.DataFrame(rows).sort_values("recording").reset_index(drop=True)
    if recordings is None and holdout_only:
        if len(out) != 38 or out.subject.nunique() != 19:
            raise RuntimeError(f"Locked holdout must be 38 recordings / 19 subjects, got {len(out)} / {out.subject.nunique()}")
        if out.subject.isin(PILOT_SUBJECTS).any():
            raise RuntimeError("Pilot leakage into locked holdout")
        if not (out.groupby("subject").size() == 2).all():
            raise RuntimeError("Expected exactly two nights per holdout participant")
        if not (out.groupby("subject").condition.nunique() == 2).all():
            raise RuntimeError("Expected placebo + temazepam per holdout participant")
    return out


def record_contract(row, idx, base_path, base_sha, script_sha, receipt_sha, B, seed, variants):
    return {
        "analysis_id": ANALYSIS_ID,
        "base_runner": base_path.name,
        "base_runner_sha256": base_sha,
        "orchestrator_sha256": script_sha,
        "receipt_sha256": receipt_sha,
        "B": int(B),
        "master_seed": int(seed),
        "record_index": int(idx),
        "record_seed": int(seed + 10007 * idx),
        "variants": list(variants),
        "recording": str(row.recording),
        "subject": int(row.subject),
        "condition": str(row.condition),
        "psg_file": Path(row.psg).name,
        "hyp_file": Path(row.hypnogram).name,
        "psg_bytes": int(Path(row.psg).stat().st_size),
        "hyp_bytes": int(Path(row.hypnogram).stat().st_size),
        "psg_sha1": hash_file(Path(row.psg), "sha1"),
        "hyp_sha1": hash_file(Path(row.hypnogram), "sha1"),
        "psg_sha256": hash_file(Path(row.psg), "sha256"),
        "hyp_sha256": hash_file(Path(row.hypnogram), "sha256"),
    }


def _same_json(a, b):
    return json.dumps(a, sort_keys=True, separators=(",", ":")) == json.dumps(b, sort_keys=True, separators=(",", ":"))


def validate_checkpoint(recdir: Path, contract, B, variants):
    pp = recdir / "RUN_PROVENANCE.json"
    sp = recdir / "SUMMARY.json"
    if not pp.exists() or not sp.exists():
        return False, "missing provenance/summary"
    try:
        old = json.loads(pp.read_text())
        if not _same_json(old, contract):
            return False, "provenance mismatch"
        summ = json.loads(sp.read_text())
        if summ.get("statistic_version") != "v3-common-support":
            return False, "summary statistic_version mismatch"
        for v in variants:
            cp = recdir / f"{v}_TCS_NULL.csv"
            jp = recdir / f"{v}_SUMMARY.json"
            if not cp.exists() or not jp.exists():
                return False, f"missing variant checkpoint {v}"
            d = pd.read_csv(cp)
            if list(d.columns).count("T_cs") != 1 or len(d) != B:
                return False, f"invalid null schema/length for {v}"
            js = json.loads(jp.read_text())
            if js.get("variant") != v or int(js.get("B", -1)) != B or js.get("statistic") != "T_cs":
                return False, f"invalid summary contract for {v}"
        return True, "exact provenance and checkpoint schema match"
    except Exception as e:
        return False, f"checkpoint validation error: {type(e).__name__}: {e}"


def analyze_recording(base, row, idx, out_dir: Path, base_path: Path, base_sha, script_sha, receipt_sha,
                      B, seed, variants, overwrite=False):
    rec = row.recording
    recdir = out_dir / rec
    recdir.mkdir(parents=True, exist_ok=True)
    contract = record_contract(row, idx, base_path, base_sha, script_sha, receipt_sha, B, seed, variants)
    ok, why = validate_checkpoint(recdir, contract, B, variants)
    if ok:
        print(f"[{rec}] checkpoint REUSED — {why}", flush=True)
        return json.loads((recdir / "SUMMARY.json").read_text())
    if any(recdir.iterdir()):
        if not overwrite:
            raise RuntimeError(f"{rec}: stale/incompatible checkpoint ({why}); rerun with --overwrite-recording")
        shutil.rmtree(recdir)
        recdir.mkdir(parents=True, exist_ok=True)

    raw, chosen, X, df, valid, Tcs_obs, runs, tx, ty = base.extract_observed(Path(row.psg), Path(row.hypnogram))
    df.to_csv(recdir / "OBSERVED_EPOCH_METRICS.csv", index=False)
    E = df.E_eff.to_numpy(float)
    I = df.ILMI_1s.to_numpy(float)
    stages = df.stage.to_numpy(object)
    epoch_ids = df.epoch.to_numpy(int)
    kobs = df["K4_state"].fillna("").astype(str).to_numpy(object)
    _, seqs = base.n2_runs(epoch_ids, stages, valid, kobs)
    dec = base.decompose(seqs)
    legacy, _ = base.T_n2_legacy(epoch_ids, stages, valid, kobs)
    if abs(float(Tcs_obs) - float(dec["T_cs"])) > 1e-10:
        raise RuntimeError(f"{rec}: observed T_cs disagreement")
    if abs(float(legacy) - float(dec["T_v2"])) > 1e-10:
        raise RuntimeError(f"{rec}: legacy decomposition disagreement")
    raw_runs = base.build_n2_raw_runs(X, df, runs, 3000)
    k_n2, tx2, ty2 = base.make_k4(E, I, valid, stages, "n2")
    Tcs_n2thr, _ = base.T_n2(epoch_ids, stages, valid, k_n2)

    variant_summaries = []
    rec_seed = seed + 10007 * idx
    for j, v in enumerate(variants):
        d, s = base.run_variant(df, valid, E, I, stages, epoch_ids, raw_runs, v, B, rec_seed + 100000 * j)
        d = d.rename(columns={"T_N2": "T_cs"})
        if "T_cs" not in d or len(d) != B:
            raise RuntimeError(f"{rec}/{v}: null output schema failure")
        s2 = dict(s)
        s2["statistic"] = "T_cs"
        s2["T_cs_observed"] = float(s2.pop("T_observed"))
        s2["null_column"] = "T_cs"
        d.to_csv(recdir / f"{v}_TCS_NULL.csv", index=False)
        (recdir / f"{v}_SUMMARY.json").write_text(json.dumps(s2, indent=2, allow_nan=True))
        variant_summaries.append(s2)

    summary = {
        "analysis_id": ANALYSIS_ID,
        "statistic_version": "v3-common-support",
        "recording": rec,
        "subject": int(row.subject),
        "night": int(row.night),
        "condition": str(row.condition),
        "channels": chosen,
        "n_observed_valid": int(valid.sum()),
        "n_N2_epochs": int(sum(len(r) for r in runs)),
        "n_N2_runs": len(runs),
        "n_C": int(dec["n_C"]),
        "T_cs_observed": float(dec["T_cs"]),
        "CMI_nats": float(dec["CMI_nats"]),
        "CMI_MM_nats": float(dec["CMI_MM_nats"]),
        "df_eff": int(dec["df_eff"]),
        "T_v2_legacy": float(dec["T_v2"]),
        "R_runstart": float(dec["R_runstart"]),
        "G_het": float(dec["G_het"]),
        "global_E_threshold": float(tx),
        "global_ILMI_threshold": float(ty),
        "N2_E_threshold": float(tx2),
        "N2_ILMI_threshold": float(ty2),
        "T_cs_N2specific_threshold": float(Tcs_n2thr),
        "variants": variant_summaries,
        "psg_sha1": contract["psg_sha1"],
        "hyp_sha1": contract["hyp_sha1"],
        "psg_sha256": contract["psg_sha256"],
        "hyp_sha256": contract["hyp_sha256"],
    }
    if rec == "ST7022":
        summary["ST7022_legacy_regression_abs_error"] = abs(float(legacy) - EXPECTED_ST7022_T_V2)
        if summary["ST7022_legacy_regression_abs_error"] > 1e-6:
            raise RuntimeError(f"ST7022 legacy regression failed: {legacy}")
    (recdir / "SUMMARY.json").write_text(json.dumps(summary, indent=2, allow_nan=True))
    # Provenance is written LAST so its presence means the record checkpoint is complete.
    (recdir / "RUN_PROVENANCE.json").write_text(json.dumps(contract, indent=2))
    del X, raw_runs, raw
    gc.collect()
    return summary


def participant_group_analysis(out_dir: Path, inv, variants, B, meta_draws, seed):
    rows, nulls = [], {}
    for r in inv.itertuples(index=False):
        s = json.loads((out_dir / r.recording / "SUMMARY.json").read_text())
        for v in variants:
            vs = next(x for x in s["variants"] if x["variant"] == v)
            rows.append({
                "recording": r.recording, "subject": int(r.subject), "condition": r.condition,
                "variant": v, "T_cs_obs": s["T_cs_observed"], "CMI_nats": s["CMI_nats"],
                "CMI_MM_nats": s["CMI_MM_nats"], "p_recording": vs["plus1_p"],
                "z_recording": vs["z_vs_null"],
            })
            nulls[(r.recording, v)] = pd.read_csv(out_dir / r.recording / f"{v}_TCS_NULL.csv")["T_cs"].to_numpy(float)
    rec = pd.DataFrame(rows)
    rec.to_csv(out_dir / "RECORDING_SIGNAL_NULL_SUMMARY.csv", index=False)
    rng = np.random.default_rng(seed)
    group = []
    for v in variants:
        rv = rec[rec.variant == v].copy()
        subj = []
        for s, g in rv.groupby("subject"):
            p = g.p_recording.to_numpy(float)
            if len(p) != 2:
                raise RuntimeError(f"subject {s}: expected 2 nights")
            ps = min(1.0, 2 * float(np.min(p)))
            subj.append({"subject": int(s), "variant": v, "p_subject_bonf": ps, "mean_z": float(g.z_recording.mean())})
        sdf = pd.DataFrame(subj)
        sdf.to_csv(out_dir / f"SUBJECT_{v}.csv", index=False)
        pp = np.clip(sdf.p_subject_bonf.to_numpy(), np.finfo(float).tiny, 1)
        Fobs = float(-2 * np.log(pp).sum())
        chi = float(stats.chi2.sf(Fobs, 2 * len(pp)))
        fnull = np.empty(meta_draws)
        recs = list(rv.recording)
        subjs = sorted(rv.subject.unique())
        for b in range(meta_draws):
            pnight = {}
            for recname in recs:
                arr = nulls[(recname, v)]
                k = int(rng.integers(len(arr)))
                t = arr[k]
                pnight[recname] = (1 + int(np.sum(arr >= t))) / (len(arr) + 1)
            psub = []
            for s in subjs:
                names = rv.loc[rv.subject == s, "recording"].tolist()
                psub.append(min(1.0, 2 * min(pnight[names[0]], pnight[names[1]])))
            fnull[b] = -2 * np.log(np.clip(psub, np.finfo(float).tiny, 1)).sum()
        pemp = float((1 + np.sum(fnull >= Fobs)) / (meta_draws + 1))
        group.append({
            "variant": v, "statistic": "T_cs", "n_subjects": len(sdf), "B_per_recording": B,
            "observed_fisher": Fobs, "chi2_reference_p_descriptive": chi,
            "empirical_meta_null_p": pemp, "meta_draws": meta_draws,
            "meta_null_mean": float(fnull.mean()), "meta_null_q95": float(np.quantile(fnull, .95)),
            "mean_subject_z": float(sdf.mean_z.mean()),
        })
    gdf = pd.DataFrame(group)
    gdf.to_csv(out_dir / "GROUP_SIGNAL_NULL_SUMMARY.csv", index=False)
    return rec, gdf


def run_audits(inv, out_dir: Path, B, meta_draws, variants, expected_contracts, production=True):
    audits = []
    def add(name, passed, detail):
        audits.append({"audit": name, "passed": bool(passed), "detail": str(detail)})
    full = len(inv) == 38 and inv.subject.nunique() == 19
    inv_ok = full if production else (len(inv) > 0)
    add("01 locked inventory" if production else "01 smoke inventory", inv_ok, f"{len(inv)} recordings/{inv.subject.nunique()} subjects; production={production}")
    add("02 leakage lock", not inv.subject.isin(PILOT_SUBJECTS).any(), f"excluded={sorted(PILOT_SUBJECTS)}")
    add("03 paired nights", (inv.groupby("subject").size() == 2).all() if full else True, "2 nights/participant when production")
    add("04 condition mapping", (inv.groupby("subject").condition.nunique() == 2).all() if full else True, "placebo + temazepam when production")
    hashes_ok = True
    for r in inv.itertuples(index=False):
        hashes_ok &= hash_file(Path(r.psg), "sha1") == r.psg_sha1
        hashes_ok &= hash_file(Path(r.hypnogram), "sha1") == r.hyp_sha1
    add("05 Drive receipt hashes", hashes_ok, "all local/Drive mirror SHA1 values match frozen receipt")
    st = next((r for r in inv.itertuples(index=False) if r.recording == "ST7022"), None)
    if st is None:
        add("06 ST7022 legacy regression", not full, "ST7022 absent in subset" if not full else "ST7022 missing")
    else:
        s = json.loads((out_dir / "ST7022" / "SUMMARY.json").read_text())
        add("06 ST7022 legacy regression", s.get("ST7022_legacy_regression_abs_error", 1) <= 1e-6,
            s.get("ST7022_legacy_regression_abs_error"))
    qcs = []
    for rec in inv.recording:
        s = json.loads((out_dir / rec / "SUMMARY.json").read_text())
        qcs.extend([x.get("qc", {}) for x in s["variants"]])
    max_auto = max([q.get("auto_spectrum_relerr", np.nan) for q in qcs if np.isfinite(q.get("auto_spectrum_relerr", np.nan))], default=np.nan)
    common_qc = [x.get("qc", {}) for rec in inv.recording for x in json.loads((out_dir / rec / "SUMMARY.json").read_text())["variants"] if x["variant"] in {"common_phase_run", "epochwise_common_phase"}]
    max_cross = max([q.get("cross_spectrum_relerr", np.nan) for q in common_qc if np.isfinite(q.get("cross_spectrum_relerr", np.nan))], default=np.nan)
    add("07 autospectrum preservation", np.isfinite(max_auto) and max_auto < 1e-10, max_auto)
    add("08 common-phase cross-spectrum preservation", np.isfinite(max_cross) and max_cross < 1e-10, max_cross)
    prov_ok = True
    details = []
    for rec, contract in expected_contracts.items():
        ok, why = validate_checkpoint(out_dir / rec, contract, B, variants)
        prov_ok &= ok
        if not ok:
            details.append(f"{rec}:{why}")
    add("09 provenance-locked checkpoints", prov_ok, "all exact" if prov_ok else "; ".join(details[:5]))
    g = out_dir / "GROUP_SIGNAL_NULL_SUMMARY.csv"
    if full and g.exists():
        gd = pd.read_csv(g)
        required = {"variant", "statistic", "n_subjects", "B_per_recording", "empirical_meta_null_p", "meta_draws"}
        group_ok = required.issubset(gd.columns) and set(gd.variant) == set(variants) and (gd.statistic == "T_cs").all() and (gd.n_subjects == 19).all() and (gd.B_per_recording == B).all() and (gd.meta_draws == meta_draws).all() and gd.empirical_meta_null_p.between(1/(meta_draws+1), 1).all()
        detail = f"rows={len(gd)}, variants={sorted(gd.variant.tolist())}"
    elif full:
        group_ok, detail = False, "group summary missing"
    else:
        group_ok, detail = True, "subset/smoke: group inference intentionally skipped"
    add("10 group calibration schema", group_ok, detail)
    adf = pd.DataFrame(audits)
    adf.to_csv(out_dir / "AUDIT_10X.csv", index=False)
    (out_dir / "AUDIT_10X.json").write_text(json.dumps(audits, indent=2))
    return adf


def deterministic_zip(out_dir: Path, zip_path: Path):
    fixed = (2026, 9, 26, 0, 0, 0)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(out_dir.rglob("*")):
            if not p.is_file():
                continue
            zi = zipfile.ZipInfo(str(p.relative_to(out_dir)).replace(os.sep, "/"), fixed)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, p.read_bytes())
    return zip_path


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parent
    ap.add_argument("--base-runner", default=str(here / "BM-A004__CFI_ST44_RAW_SIGNAL_NULL_V3CS_AUDITED.py"))
    ap.add_argument("--raw-dir", required=True, help="Drive/local directory containing the 88 verified ST44 EDF files")
    ap.add_argument("--receipt", required=True, help="Frozen ST44_DOWNLOAD_RECEIPT.csv")
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--b", type=int, default=1999)
    ap.add_argument("--seed", type=int, default=20260921)
    ap.add_argument("--meta-draws", type=int, default=100000)
    ap.add_argument("--variants", nargs="+", default=DEFAULT_VARIANTS)
    ap.add_argument("--recordings", nargs="*", default=None, help="Subset only for smoke/debug")
    ap.add_argument("--allow-subset", action="store_true")
    ap.add_argument("--overwrite-recording", action="store_true")
    args = ap.parse_args()

    base_path = Path(args.base_runner).resolve()
    raw_dir = Path(args.raw_dir).resolve()
    receipt = Path(args.receipt).resolve()
    out_root = Path(args.out_root).resolve()
    if args.recordings and not args.allow_subset:
        raise RuntimeError("--recordings requires --allow-subset; subset runs are never production-confirmatory")
    base_sha = hash_file(base_path)
    script_sha = hash_file(Path(__file__).resolve())
    receipt_sha = hash_file(receipt)
    base = load_base(base_path)
    inv = receipt_inventory(receipt, raw_dir, recordings=args.recordings, holdout_only=not bool(args.recordings))
    production = (args.recordings is None)
    out_dir = out_root / (f"BM-A005_RAW_NULL_V3CS_B{args.b}" if production else f"BM-A005_SMOKE_B{args.b}")
    out_dir.mkdir(parents=True, exist_ok=True)
    inv.to_csv(out_dir / "RAW_INVENTORY.csv", index=False)
    contract_core = {
        "analysis_id": ANALYSIS_ID,
        "status": "PRODUCTION" if production else "SMOKE_ONLY",
        "base_runner_sha256": base_sha,
        "orchestrator_sha256": script_sha,
        "receipt_sha256": receipt_sha,
        "B": args.b,
        "seed": args.seed,
        "meta_draws": args.meta_draws,
        "variants": args.variants,
        "recordings": inv.recording.tolist(),
        "n_recordings": int(len(inv)),
        "n_subjects": int(inv.subject.nunique()),
        "raw_dir": str(raw_dir),
    }
    contract_path = out_dir / "RUN_CONTRACT.json"
    old_contract = None
    if contract_path.exists():
        try:
            old_contract = json.loads(contract_path.read_text())
        except Exception:
            old_contract = None
    stable_old = None
    if old_contract is not None:
        old_core = {k: old_contract.get(k) for k in contract_core}
        if _same_json(old_core, contract_core):
            stable_old = old_contract
    contract = dict(contract_core)
    contract["timestamp_start"] = stable_old.get("timestamp_start") if stable_old else now_iso()
    if stable_old and "timestamp_end" in stable_old:
        contract["timestamp_end"] = stable_old["timestamp_end"]
    contract_path.write_text(json.dumps(contract, indent=2))
    expected = {}
    for i, row in enumerate(inv.itertuples(index=False)):
        print(f"[{i+1:02d}/{len(inv)}] {row.recording}", flush=True)
        rc = record_contract(row, i, base_path, base_sha, script_sha, receipt_sha, args.b, args.seed, args.variants)
        expected[row.recording] = rc
        analyze_recording(base, row, i, out_dir, base_path, base_sha, script_sha, receipt_sha,
                          args.b, args.seed, args.variants, overwrite=args.overwrite_recording)
    if production:
        participant_group_analysis(out_dir, inv, args.variants, args.b, args.meta_draws, args.seed + 900000)
    audits = run_audits(inv, out_dir, args.b, args.meta_draws, args.variants, expected, production=production)
    if not audits.passed.all():
        raise RuntimeError("BM-A005 audit failed:\n" + audits.to_string(index=False))
    if "timestamp_end" not in contract:
        contract["timestamp_end"] = now_iso()
    contract["audit_all_pass"] = True
    contract_path.write_text(json.dumps(contract, indent=2))
    zp = deterministic_zip(out_dir, out_root / f"{out_dir.name}.zip")
    print(audits.to_string(index=False))
    print("PACKAGE:", zp)
    print("SHA256:", hash_file(zp))


if __name__ == "__main__":
    main()
