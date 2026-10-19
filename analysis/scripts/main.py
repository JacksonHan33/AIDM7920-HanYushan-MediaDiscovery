import sys
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json
from pathlib import Path

ROOT = Path("/tmp/phase1_output")
CSV = Path("/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery/data/cleaned/survey.csv")
FIGS = Path("/tmp/phase1_output/figures")
RESULTS = Path("/tmp/phase1_output/results.md")
JSON_OUT = Path("/tmp/phase1_output/results.json")
FIGS.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Phase 1 Analysis — VibePick vs MoodFlix within-subjects")
print("=" * 70)

df = pd.read_csv(CSV)
print(f"\n[1] Loaded {len(df)} responses")

df.columns = [c.strip() for c in df.columns]

# Map columns by position (0-indexed)
COL_PROTO1 = df.columns[12]
COL_TIME1  = df.columns[13]
COL_SAT1   = df.columns[14]
COL_TRAN1  = df.columns[15]
COL_TRU1   = df.columns[16]
COL_FILLER = df.columns[17]
COL_PROTO2 = df.columns[18]
COL_TIME2  = df.columns[19]
COL_SAT2   = df.columns[20]
COL_TRAN2  = df.columns[21]
COL_TRU2   = df.columns[22]
COL_COMP   = df.columns[23]
COL_WHY    = df.columns[24]

def to_num(x):
    try: return float(x)
    except: return np.nan

df["time1_n"]  = df[COL_TIME1].apply(to_num)
df["time2_n"]  = df[COL_TIME2].apply(to_num)
df["sat1_n"]   = pd.to_numeric(df[COL_SAT1], errors="coerce")
df["sat2_n"]   = pd.to_numeric(df[COL_SAT2], errors="coerce")
df["trans1_n"] = pd.to_numeric(df[COL_TRAN1], errors="coerce")
df["trans2_n"] = pd.to_numeric(df[COL_TRAN2], errors="coerce")
df["tru1_n"]   = pd.to_numeric(df[COL_TRU1], errors="coerce")
df["tru2_n"]   = pd.to_numeric(df[COL_TRU2], errors="coerce")

def pair_vp_mf(row):
    p1 = str(row[COL_PROTO1])
    if "VibePick" in p1:
        return pd.Series({
            "vp_time": row["time1_n"], "mf_time": row["time2_n"],
            "vp_sat": row["sat1_n"],   "mf_sat": row["sat2_n"],
            "vp_trans": row["trans1_n"],"mf_trans": row["trans2_n"],
            "vp_tru": row["tru1_n"],   "mf_tru": row["tru2_n"],
        })
    else:
        return pd.Series({
            "vp_time": row["time2_n"], "mf_time": row["time1_n"],
            "vp_sat": row["sat2_n"],   "mf_sat": row["sat1_n"],
            "vp_trans": row["trans2_n"],"mf_trans": row["trans1_n"],
            "vp_tru": row["tru2_n"],   "mf_tru": row["tru1_n"],
        })

paired = df.apply(pair_vp_mf, axis=1)
clean = paired.dropna(subset=["vp_time","mf_time"])
clean = clean[(clean["vp_time"] > 0) & (clean["mf_time"] > 0)]
n = len(clean)
print(f"[2] After cleaning: n = {n} paired observations")

if n < 5:
    print("!! Too few rows, aborting")
    sys.exit(1)

vp_t = clean["vp_time"].values
mf_t = clean["mf_time"].values
diff_t = vp_t - mf_t
ratio_t = vp_t / mf_t

print(f"\n[3] Time-to-first-pick (seconds)")
print(f"    VibePick: mean={vp_t.mean():.2f}, median={np.median(vp_t):.2f}, sd={np.std(vp_t, ddof=1):.2f}, n={n}")
print(f"    MoodFlix: mean={mf_t.mean():.2f}, median={np.median(mf_t):.2f}, sd={np.std(mf_t, ddof=1):.2f}, n={n}")
print(f"    Difference (VibePick - MoodFlix): mean={diff_t.mean():.2f}, sd={np.std(diff_t, ddof=1):.2f}")

t_stat, t_p = stats.ttest_rel(vp_t, mf_t)
print(f"    Paired t-test: t({n-1}) = {t_stat:.3f}, p = {t_p:.4f}")

w_stat, w_p = stats.wilcoxon(diff_t)
print(f"    Wilcoxon signed-rank: W = {w_stat:.1f}, p = {w_p:.4f}")

cohens_dz = diff_t.mean() / np.std(diff_t, ddof=1)
print(f"    Cohen's dz (paired) = {cohens_dz:.3f}")

log_vp = np.log(vp_t)
log_mf = np.log(mf_t)
log_diff = log_vp - log_mf
t_log, p_log = stats.ttest_rel(log_vp, log_mf)
w_log, p_w_log = stats.wilcoxon(log_diff)
d_log = log_diff.mean() / log_diff.std(ddof=1)
print(f"\n    [Log-transformed time]")
print(f"    Paired t-test: t({n-1}) = {t_log:.3f}, p = {p_log:.4f}")
print(f"    Wilcoxon: p = {p_w_log:.4f}")
print(f"    Cohen's dz = {d_log:.3f} (log units)")

def paired_analysis(name, vp_arr, mf_arr):
    v = np.array(vp_arr, dtype=float)
    m = np.array(mf_arr, dtype=float)
    diff = v - m
    if len(v) < 2: return None
    t_s, t_p = stats.ttest_rel(v, m)
    try: w_s, w_p = stats.wilcoxon(diff)
    except: w_s, w_p = float("nan"), float("nan")
    sd = np.std(diff, ddof=1) if len(diff) > 1 else 0
    d = diff.mean() / sd if sd > 0 else 0
    return {
        "vp_mean": float(v.mean()), "mf_mean": float(m.mean()),
        "diff_mean": float(diff.mean()),
        "t": float(t_s), "p": float(t_p),
        "wilcoxon_p": float(w_p) if not np.isnan(w_p) else None,
        "cohens_dz": float(d),
        "n": int(len(v)),
    }

sat_results = paired_analysis("Satisfaction", clean["vp_sat"].dropna().values, clean["mf_sat"].dropna().values)
trans_results = paired_analysis("Transparency", clean["vp_trans"].dropna().values, clean["mf_trans"].dropna().values)
tru_results = paired_analysis("Trust", clean["vp_tru"].dropna().values, clean["mf_tru"].dropna().values)

print(f"\n[4] Secondary outcomes (1-7 Likert)")
for name, r in [("Satisfaction", sat_results), ("Transparency", trans_results), ("Trust", tru_results)]:
    print(f"    {name}: VibePick {r['vp_mean']:.2f} vs MoodFlix {r['mf_mean']:.2f}, "
          f"diff {r['diff_mean']:+.2f}, t={r['t']:.2f}, p={r['p']:.4f}, dz={r['cohens_dz']:.2f}, n={r['n']}")

print(f"\n[5] Comparative preference (Q23)")
comp_counts = df[COL_COMP].value_counts()
for k, v in comp_counts.items():
    print(f"    {k}: {v} ({v/len(df)*100:.1f}%)")

comp_binary = df[COL_COMP].apply(lambda x: 1 if "VibePick" in str(x) else 0 if "MoodFlix" in str(x) else None)
comp_clean = comp_binary.dropna()
if len(comp_clean) > 0:
    n_v_pick = int(comp_clean.sum())
    n_total = int(len(comp_clean))
    binom_result = stats.binomtest(n_v_pick, n_total, 0.5, alternative='two-sided')
    binom_p = float(binom_result.pvalue)
    print(f"    VibePick vs MoodFlix: {n_v_pick}/{n_total} = {n_v_pick/n_total*100:.1f}% prefer VibePick")
    print(f"    Binomial test (H0: 50/50): p = {binom_p:.4f}")
else:
    binom_p = None
    n_v_pick = 0
    n_total = 0

print(f"\n[6] Order effect (Q10 first prototype)")
order_counts = df[COL_PROTO1].value_counts()
for k, v in order_counts.items():
    print(f"    {k}: {v} ({v/len(df)*100:.1f}%)")

print(f"\n[7] Demographics (raw n = {len(df)})")
print("    Age band:")
for k, v in df[df.columns[5]].value_counts().items():
    print(f"      {k}: {v} ({v/len(df)*100:.1f}%)")
print("    Region:")
for k, v in df[df.columns[6]].value_counts().items():
    print(f"      {k}: {v} ({v/len(df)*100:.1f}%)")
print("    Hours streaming per week:")
for k, v in df[df.columns[8]].value_counts().items():
    print(f"      {k}: {v} ({v/len(df)*100:.1f}%)")

results = {
    "n_paired": int(n),
    "time_to_first_pick": {
        "vibepick_mean_sec": float(vp_t.mean()),
        "vibepick_median_sec": float(np.median(vp_t)),
        "vibepick_sd_sec": float(np.std(vp_t, ddof=1)),
        "moodflix_mean_sec": float(mf_t.mean()),
        "moodflix_median_sec": float(np.median(mf_t)),
        "moodflix_sd_sec": float(np.std(mf_t, ddof=1)),
        "diff_mean_sec": float(diff_t.mean()),
        "diff_sd_sec": float(np.std(diff_t, ddof=1)),
        "paired_t": float(t_stat), "paired_p": float(t_p),
        "wilcoxon_p": float(w_p), "cohens_dz": float(cohens_dz),
    },
    "log_time": {
        "paired_t": float(t_log), "paired_p": float(p_log),
        "wilcoxon_p": float(p_w_log), "cohens_dz": float(d_log),
    },
    "satisfaction": sat_results,
    "transparency": trans_results,
    "trust": tru_results,
    "comparative": {
        "vibepick_n": int(n_v_pick), "moodflix_n": int(n_total - n_v_pick),
        "binom_p": binom_p,
        "distribution": {k: int(v) for k, v in comp_counts.items()},
    }
}
JSON_OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"\n[8] Saved {JSON_OUT}")

# Figures
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(mf_t, vp_t, alpha=0.5, s=50, color="#2D5D8A", edgecolor="white")
lims = [0, max(vp_t.max(), mf_t.max()) * 1.1]
ax.plot(lims, lims, "k--", alpha=0.3, label="y = x (no difference)")
ax.scatter([], [], s=50, color="#2D5D8A", label="Each pair = 1 dot")
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("MoodFlix time-to-first-pick (seconds)")
ax.set_ylabel("VibePick time-to-first-pick (seconds)")
ax.set_title(f"Time-to-first-pick: VibePick vs MoodFlix (paired, n={n})\npaired t={t_stat:.2f}, p={t_p:.3f}, Cohen's dz={cohens_dz:.2f}")
ax.axhline(vp_t.mean(), color="#2D5D8A", linestyle=":", alpha=0.6, label=f"VibePick mean = {vp_t.mean():.1f}s")
ax.axvline(mf_t.mean(), color="#8A2D5D", linestyle=":", alpha=0.6, label=f"MoodFlix mean = {mf_t.mean():.1f}s")
ax.legend(loc="upper left", fontsize=8)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(FIGS / "fig1_time_paired_scatter.png", dpi=140)
plt.close(fig)
print(f"    Saved fig1_time_paired_scatter.png")

fig, ax = plt.subplots(figsize=(6, 5))
sat_v_raw = clean["vp_sat"].dropna().values
sat_m_raw = clean["mf_sat"].dropna().values
bp = ax.boxplot([sat_v_raw, sat_m_raw], labels=["VibePick", "MoodFlix"], patch_artist=True, widths=0.5)
for patch, color in zip(bp['boxes'], ["#2D5D8A", "#8A2D5D"]):
    patch.set_facecolor(color); patch.set_alpha(0.4)
for i, vals in enumerate([sat_v_raw, sat_m_raw], start=1):
    x = np.random.normal(i, 0.04, len(vals))
    ax.scatter(x, vals, alpha=0.3, s=15, color="black")
ax.set_ylabel("Satisfaction (1-7 Likert)")
ax.set_title(f"Satisfaction by prototype (n={sat_results['n']})")
ax.grid(True, alpha=0.3, axis="y")
fig.tight_layout()
fig.savefig(FIGS / "fig2_satisfaction_boxplot.png", dpi=140)
plt.close(fig)
print(f"    Saved fig2_satisfaction_boxplot.png")

fig, ax = plt.subplots(figsize=(6, 6))
comp_dict = comp_counts.to_dict()
labels = list(comp_dict.keys())
sizes = list(comp_dict.values())
colors_map = {"VibePick": "#2D5D8A", "MoodFlix": "#8A2D5D"}
colors = [colors_map.get(l, "#999999") for l in labels]
explode = [0.05] * len(labels)
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90, explode=explode)
ax.set_title(f"Comparative preference (Q23, n={len(df)})")
fig.tight_layout()
fig.savefig(FIGS / "fig3_comparative_pie.png", dpi=140)
plt.close(fig)
print(f"    Saved fig3_comparative_pie.png")

md = f"""# Phase 1 Statistical Results

> **n = {n} paired participants** (within-subjects, counterbalanced order)

## §1 Primary outcome: time-to-first-pick (seconds)

| Prototype | Mean | Median | SD | n |
|---|---|---|---|---|
| VibePick | {vp_t.mean():.2f} | {np.median(vp_t):.2f} | {np.std(vp_t, ddof=1):.2f} | {n} |
| MoodFlix | {mf_t.mean():.2f} | {np.median(mf_t):.2f} | {np.std(mf_t, ddof=1):.2f} | {n} |
| **Difference (VibePick - MoodFlix)** | **{diff_t.mean():.2f}** | - | {np.std(diff_t, ddof=1):.2f} | {n} |
| **Ratio (VibePick / MoodFlix)** | **{ratio_t.mean():.2f}** | - | {np.std(ratio_t, ddof=1):.2f} | {n} |

- **Paired t-test:** t({n-1}) = {t_stat:.3f}, **p = {t_p:.4f}**
- **Wilcoxon signed-rank:** W = {w_stat:.1f}, p = {w_p:.4f}
- **Cohen's dz (paired):** {cohens_dz:.3f}

### Log-time (for ratio interpretation)
- Paired t-test on log(time): t = {t_log:.3f}, p = {p_log:.4f}
- Wilcoxon: p = {p_w_log:.4f}
- Cohen's dz: {d_log:.3f} (log units)

## §2 Secondary outcomes (1-7 Likert)

| Outcome | VibePick mean | MoodFlix mean | Diff (V-M) | Paired t | p | Cohen's dz | n |
|---|---|---|---|---|---|---|---|
| Satisfaction | {sat_results['vp_mean']:.2f} | {sat_results['mf_mean']:.2f} | {sat_results['diff_mean']:+.2f} | {sat_results['t']:.2f} | {sat_results['p']:.4f} | {sat_results['cohens_dz']:.2f} | {sat_results['n']} |
| Transparency | {trans_results['vp_mean']:.2f} | {trans_results['mf_mean']:.2f} | {trans_results['diff_mean']:+.2f} | {trans_results['t']:.2f} | {trans_results['p']:.4f} | {trans_results['cohens_dz']:.2f} | {trans_results['n']} |
| Trust | {tru_results['vp_mean']:.2f} | {tru_results['mf_mean']:.2f} | {tru_results['diff_mean']:+.2f} | {tru_results['t']:.2f} | {tru_results['p']:.4f} | {tru_results['cohens_dz']:.2f} | {tru_results['n']} |

## §3 Comparative preference (Q23)

| Choice | n | % |
|---|---|---|
"""
for k, v in comp_counts.items():
    md += f"| {k} | {v} | {v/len(df)*100:.1f}% |\n"

if binom_p is not None:
    md += f"""
- VibePick vs MoodFlix (excluding "Hard to say"): **{n_v_pick}/{n_total} = {n_v_pick/n_total*100:.1f}%**
- **Binomial test** (H0: 50/50): **p = {binom_p:.4f}**
"""

md += f"""
## §4 Order effect (Q10 first prototype)

| First prototype | n | % |
|---|---|---|
"""
for k, v in order_counts.items():
    md += f"| {k} | {v} | {v/len(df)*100:.1f}% |\n"

md += f"""
## §5 Demographics (raw n = {len(df)})

### Age band
"""
for k, v in df[df.columns[5]].value_counts().items():
    md += f"- {k}: {v} ({v/len(df)*100:.1f}%)\n"

md += "\n### Region\n"
for k, v in df[df.columns[6]].value_counts().items():
    md += f"- {k}: {v} ({v/len(df)*100:.1f}%)\n"

md += "\n### Hours streaming per week\n"
for k, v in df[df.columns[8]].value_counts().items():
    md += f"- {k}: {v} ({v/len(df)*100:.1f}%)\n"

RESULTS.write_text(md)
print(f"\n[9] Wrote {RESULTS}")

print("\n" + "=" * 70)
print("DONE - analysis complete")
print("=" * 70)
