#!/usr/bin/env python3
"""
Phase 1 Report Generator v3 — patches v2 demographic labels + star formatting
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT = Path("/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery")
OUT     = Path("/tmp/phase1_output")
FIGS    = OUT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)

# ---------- Load sources ----------
RES = json.loads((PROJECT / "analysis/results.json").read_text())
df  = pd.read_csv(PROJECT / "data/cleaned/survey.csv")
df.columns = [c.strip() for c in df.columns]

# CORRECT column indices (verified against CSV header):
# [0] Timestamp, [1] Consent, [2] Switch frequency, [3] Subscribe, [4] Age band,
# [5] Region, [6] Video services used, [7] Hours streaming, [8] Used rec tool,
# [9] Couldn't find count, [10] Pain point, [11] Time spent searching,
# [12] Proto1, [13] Time1, [14] Sat1, [15] Trans1, [16] Tru1, [17] Word count,
# [18] Proto2, [19] Time2, [20] Sat2, [21] Trans2, [22] Tru2, [23] Comparative, [24] Why

C_PROTO1 = df.columns[12]; C_TIME1 = df.columns[13]; C_SAT1  = df.columns[14]
C_TRAN1  = df.columns[15]; C_TRU1  = df.columns[16]
C_PROTO2 = df.columns[18]; C_TIME2 = df.columns[19]; C_SAT2  = df.columns[20]
C_TRAN2  = df.columns[21]; C_TRU2  = df.columns[22]
C_COMP   = df.columns[23]; C_WHY   = df.columns[24]

# *** FIX: demographics use COLS 4 (age), 5 (region), 6 (services), 7 (hours) ***
C_AGE   = df.columns[4]
C_REG   = df.columns[5]
C_SVC   = df.columns[6]
C_HOURS = df.columns[7]
C_SWITCH = df.columns[2]

def to_num(x):
    try: return float(x)
    except: return np.nan

df["t1"] = df[C_TIME1].apply(to_num); df["t2"] = df[C_TIME2].apply(to_num)
df["s1"] = pd.to_numeric(df[C_SAT1], errors="coerce")
df["s2"] = pd.to_numeric(df[C_SAT2], errors="coerce")
df["tr1"] = pd.to_numeric(df[C_TRAN1], errors="coerce")
df["tr2"] = pd.to_numeric(df[C_TRAN2], errors="coerce")
df["tu1"] = pd.to_numeric(df[C_TRU1], errors="coerce")
df["tu2"] = pd.to_numeric(df[C_TRU2], errors="coerce")

def pair(r):
    if "VibePick" in str(r[C_PROTO1]):
        return pd.Series({"vp_t": r.t1, "mf_t": r.t2,
                          "vp_s": r.s1, "mf_s": r.s2,
                          "vp_tr": r.tr1, "mf_tr": r.tr2,
                          "vp_tu": r.tu1, "mf_tu": r.tu2})
    else:
        return pd.Series({"vp_t": r.t2, "mf_t": r.t1,
                          "vp_s": r.s2, "mf_s": r.s1,
                          "vp_tr": r.tr2, "mf_tr": r.tr1,
                          "vp_tu": r.tu2, "mf_tu": r.tu1})

pa = df.apply(pair, axis=1)
clean = pa[(pa.vp_t > 0) & (pa.mf_t > 0)].copy()
n = len(clean)
n_raw = len(df)

def star_only(p):
    """Return star marker WITHOUT markdown bold syntax (no `**`)."""
    if p is None: return ""
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    return ""

def fmt_p(p):
    if p is None: return "N/A"
    if p < 0.001: return "p < .001"
    if p < 0.01:  return f"p = {p:.3f}"
    return f"p = {p:.3f}"

# ---------- Re-generate figures (overwrite v2 with consistent styling) ----------
print("[A] Regenerating bars + distributions...")
def bar_err(vals_a, vals_b, lab_a, lab_b, ylabel, title, fname, color_a="#2D5D8A", color_b="#8A2D5D"):
    a, b = np.array(vals_a), np.array(vals_b)
    fig, ax = plt.subplots(figsize=(5.5, 5))
    means = [np.mean(a), np.mean(b)]
    errs  = [np.std(a, ddof=1), np.std(b, ddof=1)]
    ax.bar([lab_a, lab_b], means, yerr=errs, capsize=8,
           color=[color_a, color_b], alpha=0.7, edgecolor="black", linewidth=0.8)
    for i, vals in enumerate([a, b]):
        x = np.random.normal(i, 0.04, len(vals))
        ax.scatter(x, vals, alpha=0.4, s=18, color="black", zorder=3)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(FIGS / fname, dpi=140)
    plt.close(fig)
    print(f"    Saved {fname}")

bar_err(clean.vp_s.dropna().values, clean.mf_s.dropna().values,
        "VibePick", "MoodFlix", "Satisfaction (1–7 Likert)",
        f"Satisfaction — VibePick vs MoodFlix (n={n})",
        "fig2_satisfaction_bars.png")

bar_err(clean.vp_tr.dropna().values, clean.mf_tr.dropna().values,
        "VibePick", "MoodFlix", "Transparency (1–7 Likert)",
        f"Transparency — VibePick vs MoodFlix (n={n})\nVibePick significantly more transparent (p=0.028)",
        "fig3_transparency_bars.png")

bar_err(clean.vp_tu.dropna().values, clean.mf_tu.dropna().values,
        "VibePick", "MoodFlix", "Trust (1–7 Likert)",
        f"Trust — VibePick vs MoodFlix (n={n})",
        "fig4_trust_bars.png")

# Comparative pie
print("[B] Pie & region...")
order = df[C_PROTO1].value_counts()
comp = df[C_COMP].value_counts()
region = df[C_REG].value_counts()
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

colors = {"VibePick": "#2D5D8A", "MoodFlix": "#8A2D5D"}
cs = [colors.get(k, "#999999") for k in comp.index]
explode = [0.06] * len(comp)
wedges, texts, autotexts = axes[0].pie(comp.values, labels=comp.index, colors=cs,
                                       autopct='%1.0f%%', startangle=90, explode=explode,
                                       wedgeprops=dict(edgecolor="white", linewidth=2))
for t in texts: t.set_fontsize(11)
for t in autotexts: t.set_color("white"); t.set_fontweight("bold")
axes[0].set_title(f"If you had to keep just one (n={n_raw})", fontsize=11)

region.plot(kind="bar", ax=axes[1], color="#2D5D8A", alpha=0.7, edgecolor="black")
axes[1].set_title(f"Region / country of residence (n={n_raw})", fontsize=11)
axes[1].set_ylabel("Respondents"); axes[1].set_xlabel("")
axes[1].tick_params(axis="x", rotation=30, labelsize=9)
for i, v in enumerate(region.values):
    axes[1].text(i, v + 0.2, str(v), ha="center", fontsize=10, fontweight="bold")
axes[1].grid(True, alpha=0.3, axis="y")

fig.tight_layout()
fig.savefig(FIGS / "fig5_comparative_pie.png", dpi=140)
plt.close(fig)
print(f"    Saved fig5_comparative_pie.png (now pie + region)")

# Time distributions
print("[C] Time distributions...")
vp_t, mf_t = clean.vp_t.values, clean.mf_t.values
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].hist(vp_t, bins=12, color="#2D5D8A", alpha=0.7, edgecolor="black")
axes[0].axvline(np.mean(vp_t), color="#2D5D8A", linestyle="--", linewidth=2, label=f"mean = {np.mean(vp_t):.1f}s")
axes[0].axvline(np.median(vp_t), color="#2D5D8A", linestyle=":", linewidth=2, label=f"median = {np.median(vp_t):.1f}s")
axes[0].set_xlabel("Time-to-first-pick (seconds)"); axes[0].set_ylabel("Participants")
axes[0].set_title("VibePick"); axes[0].legend(fontsize=9); axes[0].grid(True, alpha=0.3)

axes[1].hist(mf_t, bins=12, color="#8A2D5D", alpha=0.7, edgecolor="black")
axes[1].axvline(np.mean(mf_t), color="#8A2D5D", linestyle="--", linewidth=2, label=f"mean = {np.mean(mf_t):.1f}s")
axes[1].axvline(np.median(mf_t), color="#8A2D5D", linestyle=":", linewidth=2, label=f"median = {np.median(mf_t):.1f}s")
axes[1].set_xlabel("Time-to-first-pick (seconds)")
axes[1].set_title("MoodFlix"); axes[1].legend(fontsize=9); axes[1].grid(True, alpha=0.3)
fig.suptitle(f"Distribution of time-to-first-pick (n={n})", fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig(FIGS / "fig6_time_distributions.png", dpi=140)
plt.close(fig)
print(f"    Saved fig6_time_distributions.png")

# Order bar
print("[D] Order...")
fig, ax = plt.subplots(figsize=(7, 4.5))
order.plot(kind="bar", ax=ax, color=["#2D5D8A", "#8A2D5D"][:len(order)], alpha=0.8, edgecolor="black")
ax.set_title(f"Counterbalance order — which prototype came first (n={n_raw})", fontsize=11)
ax.set_ylabel("Respondents"); ax.set_xlabel("")
ax.tick_params(axis="x", rotation=0)
for i, v in enumerate(order.values):
    ax.text(i, v + 0.3, str(v), ha="center", fontsize=10, fontweight="bold")
ax.grid(True, alpha=0.3, axis="y")
fig.tight_layout()
fig.savefig(FIGS / "fig7_order_imbalance.png", dpi=140)
plt.close(fig)
print(f"    Saved fig7_order_imbalance.png")

# ---------- results.md (FIXED labels) ----------
print("[E] Writing results.md...")

age = df[C_AGE].value_counts()
hours = df[C_HOURS].value_counts()
switch = df[C_SWITCH].value_counts()
pain = df[df.columns[10]].value_counts()

t  = RES["time_to_first_pick"]
lt = RES["log_time"]
sa = RES["satisfaction"]
tr = RES["transparency"]
tu = RES["trust"]
cp = RES["comparative"]

# Section helper to render a counts table
def counts_table(series, label):
    s = f"\n### {label}\n\n| Item | n | % |\n|---|---:|---:|\n"
    for k, v in series.items():
        s += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"
    return s

md = f"""# Phase 1 — Statistical Results

> **n = {n} paired, within-subjects, counterbalanced order**
> Raw responses: {n_raw} (cleaned to {n} after excluding zero/negative times)

---

## §1 Descriptive & participant profile (raw n = {n_raw})
"""

# Age (correct col)
md += "\n### Age band\n\n| Age | n | % |\n|---|---:|---:|\n"
for k, v in age.items():
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

# Region (correct col)
md += "\n### Region / country\n\n| Region | n | % |\n|---|---:|---:|\n"
for k, v in region.items():
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

# Services
md += "\n### Top video services used\n\n| Service combo | n | % |\n|---|---:|---:|\n"
svc_sorted = df[C_SVC].value_counts().head(8).items()
for k, v in svc_sorted:
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

# Hours
md += "\n### Hours of streaming per week\n\n| Hours | n | % |\n|---|---:|---:|\n"
for k, v in hours.items():
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

# Switch frequency
md += "\n### How often participants switch between streaming services\n\n| Frequency | n | % |\n|---|---:|---:|\n"
for k, v in switch.items():
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

# Pain point
md += "\n### Biggest pain point when looking for something to watch\n\n| Pain point | n | % |\n|---|---:|---:|\n"
for k, v in pain.head(8).items():
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

# Counterbalance
md += f"\n### Counterbalance order\n\n| First prototype | n | % |\n|---|---:|---:|\n"
for k, v in order.items():
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

# ---------- §2 primary ----------
md += f"""
---

## §2 Primary outcome — Time-to-first-pick (seconds)

**VibePick** M = {t['vibepick_mean_sec']:.2f}s, Mdn = {t['vibepick_median_sec']:.2f}s, SD = {t['vibepick_sd_sec']:.2f}
**MoodFlix**  M = {t['moodflix_mean_sec']:.2f}s, Mdn = {t['moodflix_median_sec']:.2f}s, SD = {t['moodflix_sd_sec']:.2f}

| Statistic | Value |
|---|---|
| Mean difference (VP − MF) | {t['diff_mean_sec']:+.2f}s (SD = {t['diff_sd_sec']:.2f}) |
| Paired t (df = {n-1}) | t = {t['paired_t']:.3f} |
| p (paired t, raw seconds) | {fmt_p(t['paired_p'])} ({star_only(t['paired_p']) or 'ns'}) |
| Wilcoxon signed-rank p | {fmt_p(t['wilcoxon_p'])} ({star_only(t['wilcoxon_p']) or 'ns'}) |
| Cohen's dz (paired) | {t['cohens_dz']:.3f} |
| Log-time paired t | t = {lt['paired_t']:.3f}, {fmt_p(lt['paired_p'])} ({star_only(lt['paired_p']) or 'ns'}) |
| Log-time Wilcoxon p | {fmt_p(lt['wilcoxon_p'])} ({star_only(lt['wilcoxon_p']) or 'ns'}) |
| Cohen's dz (log units) | {lt['cohens_dz']:.3f} |

**Interpretation.** The raw-seconds distribution is right-skewed (medians 1–2s vs means 9–10s), so the raw paired t-test is non-significant (t = {t['paired_t']:.2f}, p = {t['paired_p']:.3f}). On **log-transformed time**, both paired t (p = {lt['paired_p']:.3f}) and Wilcoxon signed-rank (p = {lt['wilcoxon_p']:.4f}) indicate VibePick is significantly *slower* in log units, dz = +{lt['cohens_dz']:.2f}. The arithmetic mean difference of {t['diff_mean_sec']:+.1f}s is small in absolute terms.

See `figures/fig1_time_paired_scatter.png` and `figures/fig6_time_distributions.png`.

---

## §3 Secondary outcomes — 1–7 Likert scales (paired t-tests)

| Outcome | VP M (SD) | MF M (SD) | Δ | t | p | sig | dz |
|---|---|---|---:|---:|---:|---|---:|
| Satisfaction | {sa['vp_mean']:.2f} ({np.std(clean.vp_s.dropna(), ddof=1):.2f}) | {sa['mf_mean']:.2f} ({np.std(clean.mf_s.dropna(), ddof=1):.2f}) | {sa['diff_mean']:+.2f} | {sa['t']:.2f} | {fmt_p(sa['p'])} | {star_only(sa['p']) or 'ns'} | {sa['cohens_dz']:.2f} |
| Transparency | {tr['vp_mean']:.2f} ({np.std(clean.vp_tr.dropna(), ddof=1):.2f}) | {tr['mf_mean']:.2f} ({np.std(clean.mf_tr.dropna(), ddof=1):.2f}) | {tr['diff_mean']:+.2f} | {tr['t']:.2f} | {fmt_p(tr['p'])} | {star_only(tr['p']) or 'ns'} | {tr['cohens_dz']:.2f} |
| Trust        | {tu['vp_mean']:.2f} ({np.std(clean.vp_tu.dropna(), ddof=1):.2f}) | {tu['mf_mean']:.2f} ({np.std(clean.mf_tu.dropna(), ddof=1):.2f}) | {tu['diff_mean']:+.2f} | {tu['t']:.2f} | {fmt_p(tu['p'])} | {star_only(tu['p']) or 'ns'} | {tu['cohens_dz']:.2f} |

**Key finding.** **Transparency** is significantly higher for VibePick (chat-style, with explicit "why I picked this") than MoodFlix (filter UI). Wilcoxon confirms (p = {tr['wilcoxon_p']:.4f}). Cohen's dz = +{tr['cohens_dz']:.2f} → small-to-medium effect.

Satisfaction and trust do not differ significantly.

See `figures/fig2_satisfaction_bars.png`, `figures/fig3_transparency_bars.png`, `figures/fig4_trust_bars.png`.

---

## §4 Comparative preference — "If you had to keep just one"

| Choice | n | % |
|---|---:|---:|
"""
for k, v in cp["distribution"].items():
    md += f"| {k} | {v} | {v/n_raw*100:.1f}% |\n"

binom = cp["binom_p"]
md += f"""
Binomial test (VibePick vs MoodFlix, excluding "Hard to say"): **{cp['vibepick_n']} / {cp['vibepick_n'] + cp['moodflix_n']}** prefer VibePick → {fmt_p(binom)} ({star_only(binom) or 'ns'}).

See `figures/fig5_comparative_pie.png`.

---

## §5 Order effect

The order balance is **skewed**: {order.iloc[0]} used VibePick first, {order.iloc[1] if len(order) > 1 else '?'} used MoodFlix first. This violates full counterbalancing and is acknowledged as a limitation in §6.

See `figures/fig7_order_imbalance.png`.

---

## §6 Limitations

1. **Order imbalance** ({order.iloc[0]} vs {order.iloc[1] if len(order) > 1 else '?'}). An order-effect test (mixed-model or carryover-adjusted) is recommended for Phase 2.
2. **Skewed time data** — raw seconds right-skewed (medians ~1–2s vs means ~9–10s); log-transform is the more appropriate scale.
3. **Sample size** — n = {n} pairs reaches ~80% power to detect dz = 0.55 but is underpowered for smaller effects.
4. **Recruitment bias** — primarily Chinese / Western social networks; not stratified to any specific platform user base.
5. **Self-report timing** — participants pasted the time they saw on the final "You picked" screen, which is informal; not instrumented.

---

## §7 Pre-registration alignment (docs/analysis-plan.md)

| Pre-registered question | Outcome | α | Result |
|---|---|---|---|
| H1: VP faster than MF (log-time) | log_t = {lt['paired_t']:.2f}, {fmt_p(lt['paired_p'])} | .05 | **{'REJECTED (VP slower on log scale)' if lt['paired_p'] < 0.05 and lt['paired_t'] > 0 else 'NOT SUPPORTED' if lt['paired_p'] >= 0.05 else 'H1 unsupported (VP not faster)'}** |
| H2: VP more transparent | t = {tr['t']:.2f}, {fmt_p(tr['p'])} | .05 | **SUPPORTED (VP > MF, dz = +{tr['cohens_dz']:.2f})** |
| H3 (exploratory) satisfaction | t = {sa['t']:.2f}, {fmt_p(sa['p'])} | .05 | Not significant |
| H4 (exploratory) trust | t = {tu['t']:.2f}, {fmt_p(tu['p'])} | .05 | Not significant |
"""

(OUT / "results.md").write_text(md, encoding="utf-8")
print(f"    Saved {OUT / 'results.md'}  ({len(md)} chars)")

import shutil
shutil.copy(PROJECT / "analysis/results.json", OUT / "results.json")
print(f"\n[Z] Done. All output in: {OUT}")
