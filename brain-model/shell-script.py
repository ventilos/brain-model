#!/usr/bin/env python3
"""
CFI / ST44 signal-level surrogate hierarchy for Sleep-EDF Expanded / Sleep Telemetry.

Purpose
-------
Run the frozen ST44 E_eff x ILMI(1 s) -> K4 -> Markov(2) vs Markov(1) pipeline
on raw Sleep Telemetry EDF recordings and test the post-hoc N2 localization against
stronger continuous-signal surrogate nulls.

Primary population unit: participant.
Locked retrospective holdout: all subjects except {21, 22, 24}.
This code does not relabel the analysis as prospective or confirm full C-field theory.

Surrogate variants
------------------
1. common_phase_run:
   Same Fourier phase shift at each frequency for all 4 channels within each
   contiguous N2 run. Preserves channel auto-spectra AND the complete complex
   cross-spectrum of each run.

2. independent_channel_phase:
   Independent phase randomization by channel within each N2 run. Preserves
   each channel auto-spectrum but destroys cross-channel phase relations.

3. epochwise_common_phase:
   Common phase randomization across channels, independently for each 30-s
   N2 epoch. Preserves within-epoch multichannel auto/cross spectra but breaks
   long-run phase continuity across epoch boundaries.

The whole-night global medians defining K4 are recomputed in every surrogate
replicate after replacing only the N2 metrics. Other-stage observed metrics
remain fixed. The observed-valid epoch mask is frozen for every surrogate.
"""

from __future__ import annotations
import argparse, gc, hashlib, json, math, os, re, sys, time, zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy import signal, stats
import mne

mne.set_log_level("ERROR")

BASE_URL = "https://physionet.org/files/sleep-edfx/1.0.0"
REQ = ["EEG Fpz-Cz", "EEG Pz-Oz", "EOG horizontal", "EMG submental"]
STAGE_MAP = {
    "Sleep stage W":"W", "Sleep stage R":"R", "Sleep stage 1":"1",
    "Sleep stage 2":"2", "Sleep stage 3":"3", "Sleep stage 4":"4",
    "Sleep stage M":"M", "Sleep stage ?":"?"
}
VALID_RAW_STAGES = {"W","R","1","2","3","4"}
MERGED_STAGES = ["W","R","1","2","N3"]
STATE_NAMES = ["LL","LH","HL","HH"]
S2I = {s:i for i,s in enumerate(STATE_NAMES)}
PILOT_SUBJECTS = {21,22,24}
EXPECTED_ST7022_T_N2 = 146.4779585335193
DEFAULT_VARIANTS = ["common_phase_run","independent_channel_phase","epochwise_common_phase"]

def norm(s: str) -> str:
    return " ".join(str(s).strip().lower().replace("_"," ").split())

def merge_stage(x):
    return "N3" if str(x) in ("3","4") else str(x)

def sha256(path: Path, chunk=8*1024*1024):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        while True:
            b=f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def download_text(url, timeout=120):
    r=requests.get(url,timeout=timeout)
    r.raise_for_status()
    return r.text

def hash_manifest():
    txt=download_text(f"{BASE_URL}/SHA256SUMS.txt")
    out={}
    for ln in txt.splitlines():
        if not ln.strip(): continue
        h,p=ln.split(maxsplit=1)
        out[p.strip()]=h.strip().lower()
    return out

def remote_pairs_from_manifest(H):
    psg=[p for p in H if re.fullmatch(r"sleep-telemetry/ST7\d{2}[12]J0-PSG\.edf",p)]
    rows=[]
    for p in sorted(psg):
        rec=Path(p).name[:6]
        cand=[q for q in H if q.startswith(f"sleep-telemetry/{rec}J") and q.endswith("-Hypnogram.edf")]
        if len(cand)!=1:
            raise RuntimeError(f"{rec}: expected exactly one hypnogram in manifest, got {cand}")
        rows.append({"recording":rec,"psg_rel":p,"hyp_rel":cand[0],
                     "subject":int(rec[3:5]),"night":int(rec[5])})
    df=pd.DataFrame(rows)
    if len(df)!=44 or df.subject.nunique()!=22:
        raise RuntimeError(f"Expected 44 ST recordings / 22 subjects, got {len(df)} / {df.subject.nunique()}")
    return df

def download_verified(rel, dest: Path, expected_sha, timeout=240):
    dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists() and sha256(dest)==expected_sha:
        return dest
    part=dest.with_suffix(dest.suffix+".part")
    headers={}
    mode="wb"
    if part.exists() and part.stat().st_size>0:
        headers["Range"]=f"bytes={part.stat().st_size}-"
        mode="ab"
    with requests.get(f"{BASE_URL}/{rel}",stream=True,headers=headers,timeout=timeout) as r:
        if r.status_code==200 and mode=="ab":
            mode="wb"
        elif r.status_code not in (200,206):
            r.raise_for_status()
        with open(part,mode) as f:
            for chunk in r.iter_content(4*1024*1024):
                if chunk: f.write(chunk)
    os.replace(part,dest)
    got=sha256(dest)
    if got!=expected_sha:
        dest.unlink(missing_ok=True)
        raise RuntimeError(f"SHA256 mismatch for {rel}: expected {expected_sha}, got {got}")
    return dest

def flatten_multilevel_columns(columns):
    def clean(v):
        if v is None: return ""
        s=str(v).strip().lower()
        s=re.sub(r"[^\w]+","_",s)
        return re.sub(r"_+","_",s).strip("_")
    out=[]
    for col in columns:
        parts=[clean(p) for p in col]
        parts=[p for p in parts if p and not p.startswith("unnamed")]
        out.append("_".join(parts))
    return out

def read_telemetry_metadata(xls_path: Path):
    raw=pd.read_excel(xls_path,header=[0,1],engine="xlrd")
    raw.columns=flatten_multilevel_columns(raw.columns)
    rename={
        "subject_age_sex_nr":"subject",
        "subject_age_sex_age":"age",
        "subject_age_sex_m1_f2":"sex",
        "placebo_night_night_nr":"placebo_night",
        "placebo_night_lights_off":"placebo_lights_off",
        "temazepam_night_night_nr":"temazepam_night",
        "temazepam_night_lights_off":"temazepam_lights_off",
    }
    miss=[c for c in rename if c not in raw.columns]
    if miss: raise RuntimeError(f"Unexpected ST-subjects.xls schema; missing={miss}")
    x=raw.rename(columns=rename).copy()
    x["sex"]=x["sex"].map({1:"M",2:"F"}).fillna(x["sex"])
    rows=[]
    for _,r in x.iterrows():
        if pd.isna(r["subject"]): continue
        s=int(r["subject"])
        for cond in ("placebo","temazepam"):
            nv=r[f"{cond}_night"]
            if pd.isna(nv): continue
            rows.append({"subject":s,"age":r.get("age"),"sex":r.get("sex"),
                         "condition":cond,"night":int(nv),
                         "lights_off":r.get(f"{cond}_lights_off")})
    meta=pd.DataFrame(rows)
    if len(meta)!=44 or meta.subject.nunique()!=22:
        raise RuntimeError("Metadata integrity failure")
    if not (meta.groupby("subject").condition.nunique()==2).all():
        raise RuntimeError("Each subject must have one placebo and one temazepam night")
    return meta

def build_inventory(root: Path, holdout_only=True):
    H=hash_manifest()
    meta_rel="ST-subjects.xls"
    xls=download_verified(meta_rel,root/meta_rel,H[meta_rel])
    meta=read_telemetry_metadata(xls)
    pairs=remote_pairs_from_manifest(H).merge(meta,on=["subject","night"],how="left",validate="one_to_one")
    if pairs.condition.isna().any(): raise RuntimeError("Missing condition mapping")
    if holdout_only:
        pairs=pairs[~pairs.subject.isin(PILOT_SUBJECTS)].copy()
        if len(pairs)!=38 or pairs.subject.nunique()!=19:
            raise RuntimeError("Holdout must be 38 recordings / 19 subjects")
    return pairs.reset_index(drop=True),H

def download_inventory(pairs,H,raw_dir: Path):
    raw_dir.mkdir(parents=True,exist_ok=True)
    rows=[]
    for r in pairs.itertuples(index=False):
        psg=download_verified(r.psg_rel,raw_dir/Path(r.psg_rel).name,H[r.psg_rel])
        hyp=download_verified(r.hyp_rel,raw_dir/Path(r.hyp_rel).name,H[r.hyp_rel])
        rows.append({**r._asdict(),"psg":str(psg),"hypnogram":str(hyp),
                     "psg_sha256":sha256(psg),"hyp_sha256":sha256(hyp)})
    return pd.DataFrame(rows)

def choose_channels(ch_names):
    d={norm(x):x for x in ch_names}
    missing=[x for x in REQ if norm(x) not in d]
    if missing: raise RuntimeError(f"Missing required channels {missing}; available={ch_names}")
    return [d[norm(x)] for x in REQ]

def detrend_z(X):
    X=signal.detrend(np.asarray(X,float),axis=1,type="linear")
    X-=X.mean(axis=1,keepdims=True)
    sd=X.std(axis=1,ddof=1,keepdims=True)
    if (sd<=0).any() or not np.isfinite(sd).all():
        raise ValueError("zero/nonfinite channel SD")
    return (X/sd).T

def weighted_efficiency(R,eps=1e-12):
    W=np.abs(np.asarray(R,float)).copy()
    np.fill_diagonal(W,0)
    d=W.shape[0]
    mask=~np.eye(d,dtype=bool)
    L=np.full((d,d),np.inf)
    np.fill_diagonal(L,0)
    L[mask]=1/np.maximum(W[mask],eps)
    D=L.copy()
    for k in range(d):
        D=np.minimum(D,D[:,k,None]+D[None,k,:])
    inv=np.zeros_like(D)
    v=mask&np.isfinite(D)&(D>0)
    inv[v]=1/D[v]
    return float(inv[mask].mean()),float(W[np.triu_indices(d,1)].mean())

def gaussian_lag_mi(X,lag,ridge=0.0):
    n,d=X.shape
    if lag<=0 or lag>=n-2: raise ValueError("invalid lag")
    J=np.concatenate([X[:-lag],X[lag:]],axis=1)
    amp=np.max(np.abs(J),axis=0)
    if np.any(amp==0): raise ValueError("zero amplitude")
    Z=J/amp
    Z-=Z.mean(axis=0)
    sd=Z.std(axis=0,ddof=1)
    if np.any(sd==0): raise ValueError("zero lagged SD")
    Z/=sd
    R=(Z.T@Z)/(len(Z)-1)
    R=(R+R.T)/2
    C=R+ridge*np.eye(2*d)
    def ld(M):
        L=np.linalg.cholesky(M)
        return float(2*np.log(np.diag(L)).sum())
    mi=.5*(ld(C[:d,:d])+ld(C[d:,d:])-ld(C))
    return float(max(mi,0))

def annotations(path):
    a=mne.read_annotations(str(path))
    return [(float(o),float(o+d),STAGE_MAP.get(str(s),"?"))
            for o,d,s in zip(a.onset,a.duration,a.description)]

def stage_at(A,t):
    for a,b,s in A:
        if a<=t<b: return s
    return "?"

def make_k4(E,I,valid,stages,threshold_mode="global"):
    E=np.asarray(E,float); I=np.asarray(I,float); valid=np.asarray(valid,bool)
    q=np.full(len(E),"",dtype=object)
    sm=np.array([merge_stage(x) for x in stages],dtype=object)
    if threshold_mode=="global":
        tx=float(np.median(E[valid])); ty=float(np.median(I[valid]))
        groups=[(valid,tx,ty)]
    elif threshold_mode=="n2":
        g=valid & (sm=="2")
        tx=float(np.median(E[g])); ty=float(np.median(I[g]))
        groups=[(valid,tx,ty)]
    else:
        raise ValueError(threshold_mode)
    for g,tx,ty in groups:
        q[g&(E>=tx)&(I>=ty)]="HH"
        q[g&(E>=tx)&(I<ty)]="HL"
        q[g&(E<tx)&(I>=ty)]="LH"
        q[g&(E<tx)&(I<ty)]="LL"
    return q,tx,ty

def ll_order(seqs,order):
    counts={}
    ll=0.0
    for s in seqs:
        if len(s)<=order: continue
        for t in range(order,len(s)):
            ctx=tuple(map(int,s[t-order:t]))
            y=int(s[t])
            counts.setdefault(ctx,np.zeros(4,int))[y]+=1
    for a in counts.values():
        z=a[a>0]
        ll+=float(np.sum(z*np.log(z/a.sum())))
    return ll

def n2_runs(epoch_ids,stages,valid,k4):
    ids=np.asarray(epoch_ids,int)
    st=np.asarray([merge_stage(x) for x in stages],dtype=object)
    good=np.asarray(valid,bool)&(st=="2")&np.isin(k4,STATE_NAMES)
    pos=np.flatnonzero(good)
    if len(pos)==0: return [],[]
    runs=[]; cur=[pos[0]]
    for j in pos[1:]:
        if j==cur[-1]+1 and ids[j]==ids[cur[-1]]+1:
            cur.append(j)
        else:
            runs.append(np.array(cur,int)); cur=[j]
    runs.append(np.array(cur,int))
    seqs=[np.array([S2I[x] for x in k4[r]],np.int8) for r in runs]
    return runs,seqs

# --- BM-A002-CS-V3-REPAIR: common-support Markov(2) vs Markov(1) ---
K=4
ANALYSIS_ID="BM-A002-CS-V3-REPAIR"
def _triples(seqs, t0=2):
    a, b, c = [], [], []
    for s in seqs:
        s = np.asarray(s, dtype=np.int64)
        if len(s) <= t0:
            continue
        a.append(s[t0 - 2:-2])
        b.append(s[t0 - 1:-1])
        c.append(s[t0:])
    if not c:
        z = np.zeros(0, dtype=np.int64)
        return z, z, z
    return np.concatenate(a), np.concatenate(b), np.concatenate(c)

def _run_starts(seqs):
    x0 = np.array([int(s[0]) for s in seqs if len(s) >= 2], dtype=np.int64)
    x1 = np.array([int(s[1]) for s in seqs if len(s) >= 2], dtype=np.int64)
    return x0, x1

def _table(ctx, y, n_ctx):
    return np.bincount(ctx * K + y, minlength=n_ctx * K).reshape(n_ctx, K).astype(float)

def _ll(tab):
    rs = tab.sum(axis=1, keepdims=True)
    m = tab > 0
    return float(np.sum(tab[m] * np.log((tab / np.where(rs > 0, rs, 1.0))[m])))

def _free(tab):
    return int((tab > 0).sum() - (tab.sum(axis=1) > 0).sum())

def decompose(seqs, burn_in=0):
    a, b, c = _triples(seqs, 2 + int(burn_in))
    n_C = int(len(c))
    tab2 = _table(a * K + b, c, K * K)
    tab1 = _table(b, c, K)
    l2, l1C = _ll(tab2), _ll(tab1)
    T_cs = 2.0 * (l2 - l1C)
    df_eff = _free(tab2) - _free(tab1)
    out = {"n_runs": len(seqs), "n_C": n_C, "T_cs": T_cs, "df_eff": df_eff,
           "CMI_nats": T_cs / (2 * n_C) if n_C else float("nan"),
           "CMI_MM_nats": (T_cs - df_eff) / (2 * n_C) if n_C else float("nan")}
    if burn_in == 0:
        x0, x1 = _run_starts(seqs)
        tabE = _table(x0, x1, K)
        l1E, l1U = _ll(tabE), _ll(tab1 + tabE)
        n_E = int(len(x1))
        H_E = -l1E / n_E if n_E else 0.0
        out.update({"n_E": n_E, "H_E_nats": H_E, "R_runstart": 2.0 * n_E * H_E,
                    "G_het": 2.0 * (l1C + l1E - l1U), "T_v2": 2.0 * (l2 - l1U)})
    return out

def cs_fields(epoch_ids, stages, valid, k4, T_legacy):
    runs, seqs = n2_runs(epoch_ids, stages, valid, k4)
    d = decompose(seqs)
    out = {"statistic_version": "v3-common-support", "cs_analysis_id": ANALYSIS_ID}
    for key, val in d.items():
        out["cs_" + key] = float(val) if isinstance(val, float) else int(val)
    out["cs_legacy_abs_diff"] = abs(float(T_legacy) - d["T_v2"])
    return out

def T_n2_legacy(epoch_ids,stages,valid,k4):
    runs,seqs=n2_runs(epoch_ids,stages,valid,k4)
    return 2*(ll_order(seqs,2)-ll_order(seqs,1)),runs

def T_n2(epoch_ids,stages,valid,k4):
    runs,seqs=n2_runs(epoch_ids,stages,valid,k4)
    return decompose(seqs)["T_cs"],runs


def extract_observed(psg_path,hyp_path):
    raw=mne.io.read_raw_edf(str(psg_path),preload=False,verbose="ERROR")
    chosen=choose_channels(raw.ch_names)
    sf=float(raw.info["sfreq"])
    if abs(sf-100)>1e-9: raise RuntimeError(f"Expected 100 Hz, got {sf}")
    X=raw.get_data(picks=chosen)
    A=annotations(hyp_path)
    spe=int(round(30*sf)); ne=X.shape[1]//spe
    rows=[]
    for e in range(ne):
        st=stage_at(A,e*30+15)
        stage_valid=st in VALID_RAW_STAGES
        rec={"epoch":e,"stage":st,"stage_valid":stage_valid,"metric_valid":False,
             "E_eff":np.nan,"mean_abs_edge":np.nan,"ILMI_1s":np.nan}
        try:
            Z=detrend_z(X[:,e*spe:(e+1)*spe])
            R=np.corrcoef(Z,rowvar=False)
            ee,edge=weighted_efficiency(R)
            mi=gaussian_lag_mi(Z,int(round(sf)),0.0)
            rec.update(metric_valid=True,E_eff=ee,mean_abs_edge=edge,ILMI_1s=mi)
        except Exception:
            pass
        rows.append(rec)
    df=pd.DataFrame(rows)
    valid=(df.metric_valid&df.stage_valid).to_numpy(bool)
    k4,tx,ty=make_k4(df.E_eff.to_numpy(),df.ILMI_1s.to_numpy(),valid,df.stage.to_numpy(),"global")
    df["K4_state"]=k4
    Tobs,runs=T_n2(df.epoch.to_numpy(),df.stage.to_numpy(),valid,k4)
    return raw,chosen,X,df,valid,float(Tobs),runs,float(tx),float(ty)

def _phase_vector(nfreq,rng,even_n):
    phi=rng.uniform(0,2*np.pi,nfreq)
    phi[0]=0.0
    if even_n: phi[-1]=0.0
    return phi

def surrogate_common_phase_run(seg,rng):
    F=np.fft.rfft(seg,axis=1)
    phi=_phase_vector(F.shape[1],rng,seg.shape[1]%2==0)
    return np.fft.irfft(F*np.exp(1j*phi)[None,:],n=seg.shape[1],axis=1)

def surrogate_independent_channel_phase(seg,rng):
    F=np.fft.rfft(seg,axis=1)
    phi=rng.uniform(0,2*np.pi,F.shape)
    phi[:,0]=0.0
    if seg.shape[1]%2==0: phi[:,-1]=0.0
    return np.fft.irfft(F*np.exp(1j*phi),n=seg.shape[1],axis=1)

def surrogate_epochwise_common_phase(seg,rng,spe):
    if seg.shape[1]%spe:
        raise ValueError("N2 run not aligned to full 30-s epochs")
    n=seg.shape[1]//spe
    ep=seg.reshape(4,n,spe).transpose(1,0,2)
    F=np.fft.rfft(ep,axis=2)
    phi=rng.uniform(0,2*np.pi,(n,F.shape[2]))
    phi[:,0]=0.0
    if spe%2==0: phi[:,-1]=0.0
    y=np.fft.irfft(F*np.exp(1j*phi)[:,None,:],n=spe,axis=2)
    return y.transpose(1,0,2).reshape(4,n*spe)

def spectral_qc(seg,sur,variant,spe):
    if variant=="epochwise_common_phase":
        if seg.shape[1]%spe: raise ValueError("QC segment not epoch aligned")
        n=seg.shape[1]//spe
        a=seg.reshape(4,n,spe).transpose(1,0,2)
        b=sur.reshape(4,n,spe).transpose(1,0,2)
        F=np.fft.rfft(a,axis=2); G=np.fft.rfft(b,axis=2)
        p0=np.abs(F)**2; p1=np.abs(G)**2
        auto_err=float(np.max(np.abs(p1-p0))/max(float(np.max(p0)),1e-30))
        C0=F[:,:,None,:]*np.conj(F[:,None,:,:])
        C1=G[:,:,None,:]*np.conj(G[:,None,:,:])
        cross_err=float(np.max(np.abs(C1-C0))/max(float(np.max(np.abs(C0))),1e-30))
        return {"auto_spectrum_relerr":auto_err,"cross_spectrum_relerr":cross_err,"qc_scale":"epoch"}
    F=np.fft.rfft(seg,axis=1); G=np.fft.rfft(sur,axis=1)
    p0=np.abs(F)**2; p1=np.abs(G)**2
    auto_err=float(np.max(np.abs(p1-p0))/max(float(np.max(p0)),1e-30))
    cross_err=np.nan; cross_change=np.nan
    C0=F[:,None,:]*np.conj(F[None,:,:])
    C1=G[:,None,:]*np.conj(G[None,:,:])
    if variant=="common_phase_run":
        cross_err=float(np.max(np.abs(C1-C0))/max(float(np.max(np.abs(C0))),1e-30))
    elif variant=="independent_channel_phase":
        cross_change=float(np.linalg.norm(C1-C0)/max(float(np.linalg.norm(C0)),1e-30))
    return {"auto_spectrum_relerr":auto_err,"cross_spectrum_relerr":cross_err,"cross_spectrum_change":cross_change,"qc_scale":"run"}

def metrics_for_epochs(ep4):
    # ep4: (n_epochs,4,samples)
    E=[]; I=[]
    for ep in ep4:
        Z=detrend_z(ep)
        R=np.corrcoef(Z,rowvar=False)
        ee,_=weighted_efficiency(R)
        mi=gaussian_lag_mi(Z,100,0.0)
        E.append(ee); I.append(mi)
    return np.asarray(E),np.asarray(I)

def build_n2_raw_runs(X,df,runs,spe=3000):
    out=[]
    for r in runs:
        epoch_ids=df.epoch.to_numpy(int)[r]
        if not np.all(np.diff(epoch_ids)==1): raise RuntimeError("Noncontiguous run")
        a=int(epoch_ids[0]*spe); b=int((epoch_ids[-1]+1)*spe)
        out.append((r,X[:,a:b].copy()))
    return out

def run_variant(df,valid,Eobs,Iobs,stages,epoch_ids,raw_runs,variant,B,seed,max_attempt_factor=5):
    fn={
        "common_phase_run":surrogate_common_phase_run,
        "independent_channel_phase":surrogate_independent_channel_phase,
        "epochwise_common_phase":surrogate_epochwise_common_phase
    }[variant]
    rng=np.random.default_rng(seed)
    kobs,_,_=make_k4(Eobs,Iobs,valid,stages,"global")
    Tobs,_=T_n2(epoch_ids,stages,valid,kobs)
    out=[]; attempts=0; qc=None
    while len(out)<B and attempts<max_attempt_factor*B:
        attempts+=1
        E=Eobs.copy(); I=Iobs.copy()
        ok=True
        for idx,(r,seg) in enumerate(raw_runs):
            try:
                if variant=="epochwise_common_phase":
                    sur=fn(seg,rng,3000)
                else:
                    sur=fn(seg,rng)
                if qc is None and idx==0:
                    qc=spectral_qc(seg,sur,variant,3000)
                n=len(r)
                ep=sur.reshape(4,n,3000).transpose(1,0,2)
                ee,mi=metrics_for_epochs(ep)
                if not (np.isfinite(ee).all() and np.isfinite(mi).all()):
                    ok=False; break
                E[r]=ee; I[r]=mi
            except Exception:
                ok=False; break
        if not ok: continue
        k4,tx,ty=make_k4(E,I,valid,stages,"global")
        T,_=T_n2(epoch_ids,stages,valid,k4)
        out.append({"replicate":len(out)+1,"attempt":attempts,"T_N2":float(T),
                    "E_threshold":tx,"ILMI_threshold":ty})
    if len(out)<B:
        raise RuntimeError(f"{variant}: only {len(out)}/{B} valid replicates after {attempts} attempts")
    d=pd.DataFrame(out)
    exc=int((d.T_N2>=Tobs).sum())
    p=(1+exc)/(B+1)
    return d,{
        "variant":variant,"B":B,"T_observed":float(Tobs),
        "null_mean":float(d.T_N2.mean()),"null_sd":float(d.T_N2.std(ddof=1)),
        "null_median":float(d.T_N2.median()),
        "null_q95":float(d.T_N2.quantile(.95)),"null_q99":float(d.T_N2.quantile(.99)),
        "exceedances":exc,"plus1_p":float(p),
        "z_vs_null":float((Tobs-d.T_N2.mean())/d.T_N2.std(ddof=1)),
        "attempts":attempts,"qc":qc
    }

def analyze_recording(row,out_dir: Path,B,seed,variants):
    rec=row.recording
    recdir=out_dir/rec; recdir.mkdir(parents=True,exist_ok=True)
    done=recdir/"SUMMARY.json"
    if done.exists():
        return json.loads(done.read_text())
    raw,chosen,X,df,valid,Tobs,runs,tx,ty=extract_observed(Path(row.psg),Path(row.hypnogram))
    df.to_csv(recdir/"OBSERVED_EPOCH_METRICS.csv",index=False)
    E=df.E_eff.to_numpy(float); I=df.ILMI_1s.to_numpy(float)
    stages=df.stage.to_numpy(object); epoch_ids=df.epoch.to_numpy(int)
    raw_runs=build_n2_raw_runs(X,df,runs,3000)
    # N2 threshold ablation
    k_n2,tx2,ty2=make_k4(E,I,valid,stages,"n2")
    T_n2thr,_=T_n2(epoch_ids,stages,valid,k_n2)
    results=[]
    for j,v in enumerate(variants):
        csv=recdir/f"{v}_NULL.csv"; js=recdir/f"{v}_SUMMARY.json"
        if csv.exists() and js.exists():
            s=json.loads(js.read_text()); results.append(s); continue
        d,s=run_variant(df,valid,E,I,stages,epoch_ids,raw_runs,v,B,seed+100000*j)
        d.to_csv(csv,index=False); js.write_text(json.dumps(s,indent=2)); results.append(s)
    summary={
        "recording":rec,"subject":int(row.subject),"night":int(row.night),
        "condition":str(row.condition),"channels":chosen,
        "n_observed_valid":int(valid.sum()),"n_N2_epochs":int(sum(len(r) for r in runs)),
        "n_N2_runs":len(runs),"T_N2_observed":Tobs,
        "global_E_threshold":tx,"global_ILMI_threshold":ty,
        "N2_E_threshold":tx2,"N2_ILMI_threshold":ty2,
        "T_N2_N2specific_threshold":float(T_n2thr),
        "variants":results,
        "psg_sha256":sha256(Path(row.psg)),"hyp_sha256":sha256(Path(row.hypnogram))
    }
    T_legacy_v2,_=T_n2_legacy(epoch_ids,stages,valid,df["K4_state"].to_numpy())
    summary.update(cs_fields(epoch_ids,stages,valid,df["K4_state"].to_numpy(),T_legacy_v2))
    if rec=="ST7022":
        summary["ST7022_regression_abs_error"]=abs(T_legacy_v2-EXPECTED_ST7022_T_N2)
        if summary["ST7022_regression_abs_error"]>1e-6:
            raise RuntimeError(f"ST7022 regression failed: T_legacy_v2={T_legacy_v2} expected {EXPECTED_ST7022_T_N2}")
    done.write_text(json.dumps(summary,indent=2))
    del X,raw_runs,raw
    gc.collect()
    return summary

def participant_group_analysis(out_dir: Path,pairs,variants,B,meta_draws=50000,seed=20260921):
    rows=[]
    nulls={}
    for r in pairs.itertuples(index=False):
        recdir=out_dir/r.recording
        s=json.loads((recdir/"SUMMARY.json").read_text())
        for v in variants:
            vs=next(x for x in s["variants"] if x["variant"]==v)
            rows.append({"recording":r.recording,"subject":int(r.subject),"condition":r.condition,
                         "variant":v,"T_obs":s["T_N2_observed"],"p_recording":vs["plus1_p"],
                         "z_recording":vs["z_vs_null"]})
            nulls[(r.recording,v)]=pd.read_csv(recdir/f"{v}_NULL.csv").T_N2.to_numpy(float)
    rec=pd.DataFrame(rows)
    rec.to_csv(out_dir/"RECORDING_SIGNAL_NULL_SUMMARY.csv",index=False)
    rng=np.random.default_rng(seed)
    group=[]
    for v in variants:
        rv=rec[rec.variant==v].copy()
        subj=[]
        for s,g in rv.groupby("subject"):
            p=g.p_recording.to_numpy(float)
            if len(p)!=2: raise RuntimeError(f"subject {s}: expected 2 nights")
            ps=min(1.0,2*float(np.min(p)))
            subj.append({"subject":int(s),"variant":v,"p_subject_bonf":ps,
                         "mean_z":float(g.z_recording.mean())})
        sdf=pd.DataFrame(subj)
        sdf.to_csv(out_dir/f"SUBJECT_{v}.csv",index=False)
        pp=np.clip(sdf.p_subject_bonf.to_numpy(),np.finfo(float).tiny,1)
        Fobs=float(-2*np.log(pp).sum())
        chi=float(stats.chi2.sf(Fobs,2*len(pp)))
        # Empirical meta-null: sample one raw-signal surrogate independently per night.
        fnull=np.empty(meta_draws)
        recs=list(rv.recording)
        subjs=sorted(rv.subject.unique())
        rmap=rv.set_index("recording")
        for b in range(meta_draws):
            pnight={}
            for recname in recs:
                arr=nulls[(recname,v)]
                k=int(rng.integers(len(arr)))
                t=arr[k]
                # pseudo-observed rank p from the finite surrogate ensemble; include self -> conservative
                pnight[recname]=int(np.sum(arr>=t))/len(arr)
            psub=[]
            for s in subjs:
                names=rv.loc[rv.subject==s,"recording"].tolist()
                psub.append(min(1.0,2*min(pnight[names[0]],pnight[names[1]])))
            fnull[b]=-2*np.log(np.clip(psub,np.finfo(float).tiny,1)).sum()
        pemp=float((1+np.sum(fnull>=Fobs))/(meta_draws+1))
        group.append({"variant":v,"n_subjects":len(sdf),"B_per_recording":B,
                      "observed_fisher":Fobs,"chi2_reference_p_descriptive":chi,
                      "empirical_meta_null_p":pemp,"meta_draws":meta_draws,
                      "meta_null_mean":float(fnull.mean()),"meta_null_q95":float(np.quantile(fnull,.95)),
                      "mean_subject_z":float(sdf.mean_z.mean())})
    gdf=pd.DataFrame(group)
    gdf.to_csv(out_dir/"GROUP_SIGNAL_NULL_SUMMARY.csv",index=False)
    return rec,gdf

def run_audits(root: Path,pairs,H,out_dir: Path,B,variants):
    audits=[]
    def add(name,passed,detail): audits.append({"audit":name,"passed":bool(passed),"detail":str(detail)})
    add("01 inventory",len(pairs)==38 and pairs.subject.nunique()==19,f"{len(pairs)} recordings/{pairs.subject.nunique()} subjects")
    add("02 leakage lock",not pairs.subject.isin(PILOT_SUBJECTS).any(),f"excluded={sorted(PILOT_SUBJECTS)}")
    add("03 paired nights",(pairs.groupby("subject").size()==2).all(),"2 nights per participant")
    add("04 condition mapping",(pairs.groupby("subject").condition.nunique()==2).all(),"placebo + temazepam")
    add("05 source hashes",all(sha256(Path(r.psg))==H[r.psg_rel] and sha256(Path(r.hypnogram))==H[r.hyp_rel] for r in pairs.itertuples()),"all SHA256 match PhysioNet manifest")
    st=next((r for r in pairs.itertuples() if r.recording=="ST7022"),None)
    if st:
        s=json.loads((out_dir/"ST7022"/"SUMMARY.json").read_text())
        add("06 ST7022 frozen regression",s.get("ST7022_regression_abs_error",1)<=1e-6,s.get("ST7022_regression_abs_error"))
    else: add("06 ST7022 frozen regression",False,"ST7022 absent")
    qcs=[]
    for rec in pairs.recording:
        s=json.loads((out_dir/rec/"SUMMARY.json").read_text())
        qcs.extend([x.get("qc",{}) for x in s["variants"]])
    max_auto=max([q.get("auto_spectrum_relerr",np.nan) for q in qcs if np.isfinite(q.get("auto_spectrum_relerr",np.nan))],default=np.nan)
    max_cross=max([q.get("cross_spectrum_relerr",np.nan) for q in qcs if np.isfinite(q.get("cross_spectrum_relerr",np.nan))],default=np.nan)
    add("07 autospectrum preservation",np.isfinite(max_auto) and max_auto<1e-10,max_auto)
    add("08 common-phase cross-spectrum preservation",np.isfinite(max_cross) and max_cross<1e-10,max_cross)
    complete=all((out_dir/rec/"SUMMARY.json").exists() for rec in pairs.recording)
    add("09 checkpoint completeness",complete,f"{sum((out_dir/r/'SUMMARY.json').exists() for r in pairs.recording)}/{len(pairs)}")
    g=out_dir/"GROUP_SIGNAL_NULL_SUMMARY.csv"
    add("10 group empirical calibration",g.exists(),f"empirical meta-null present={g.exists()}; B={B}; variants={variants}")
    adf=pd.DataFrame(audits)
    adf.to_csv(out_dir/"AUDIT_10X.csv",index=False)
    (out_dir/"AUDIT_10X.json").write_text(json.dumps(audits,indent=2))
    return adf

def package_outputs(out_dir: Path):
    zp=out_dir.parent/f"{out_dir.name}.zip"
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out_dir.rglob("*")):
            if p.is_file(): z.write(p,p.relative_to(out_dir))
    return zp

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default="/content/cfi_st44")
    ap.add_argument("--b",type=int,default=999)
    ap.add_argument("--seed",type=int,default=20260921)
    ap.add_argument("--meta-draws",type=int,default=50000)
    ap.add_argument("--variants",nargs="+",default=DEFAULT_VARIANTS)
    ap.add_argument("--full44",action="store_true",help="exploratory; default is locked 19-subject holdout")
    args=ap.parse_args()
    root=Path(args.root); raw_dir=root/"raw"; out_dir=root/f"results_v3cs_B{args.b}"
    out_dir.mkdir(parents=True,exist_ok=True)
    pairs,H=build_inventory(root,holdout_only=not args.full44)
    inv=download_inventory(pairs,H,raw_dir)
    inv.to_csv(out_dir/"RAW_INVENTORY.csv",index=False)
    for i,row in enumerate(inv.itertuples(index=False)):
        print(f"[{i+1:02d}/{len(inv)}] {row.recording}",flush=True)
        analyze_recording(row,out_dir,args.b,args.seed+10007*i,args.variants)
    if not args.full44:
        participant_group_analysis(out_dir,inv,args.variants,args.b,args.meta_draws,args.seed+900000)
    audits=run_audits(root,inv,H,out_dir,args.b,args.variants)
    print(audits.to_string(index=False))
    zp=package_outputs(out_dir)
    print("PACKAGE:",zp)
    print("SHA256:",sha256(zp))

if __name__=="__main__":
    main()
