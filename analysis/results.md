# Phase 1 — Statistical Results

> **n = 28 paired, within-subjects, counterbalanced order**
> Raw responses: 31 (cleaned to 28 after excluding zero/negative times)

---

## §1 Descriptive & participant profile (raw n = 31)

### Age band

| Age | n | % |
|---|---:|---:|
| 25-34 | 12 | 38.7% |
| 15-24 | 10 | 32.3% |
| 35-44 | 7 | 22.6% |
| 45-55 | 2 | 6.5% |

### Region / country

| Region | n | % |
|---|---:|---:|
| China mainland | 9 | 29.0% |
| United States | 7 | 22.6% |
| Hong Kong SAR | 5 | 16.1% |
| United Kingdom | 4 | 12.9% |
| Japan | 3 | 9.7% |
| Other | 3 | 9.7% |

### Top video services used

| Service combo | n | % |
|---|---:|---:|
| YouTube | 6 | 19.4% |
| Netflix, Disney+, YouTube | 5 | 16.1% |
| Other | 4 | 12.9% |
| Netflix, YouTube | 2 | 6.5% |
| YouTube, Other | 2 | 6.5% |
| Netflix, Prime Video, YouTube | 2 | 6.5% |
| Netflix, Hulu, YouTube | 2 | 6.5% |
| Prime Video, YouTube | 1 | 3.2% |

### Hours of streaming per week

| Hours | n | % |
|---|---:|---:|
| 2-5 | 11 | 35.5% |
| 6-10 | 9 | 29.0% |
| 11-20 | 6 | 19.4% |
| < 2 | 3 | 9.7% |
| >20 | 2 | 6.5% |

### How often participants switch between streaming services

| Frequency | n | % |
|---|---:|---:|
| Daily | 11 | 35.5% |
| Weekly | 11 | 35.5% |
| Monthly | 5 | 16.1% |
| Rarely | 4 | 12.9% |

### Biggest pain point when looking for something to watch

| Pain point | n | % |
|---|---:|---:|
| Recommendations are bad | 9 | 29.0% |
| Don't know which service has the movie | 9 | 29.0% |
| Too many services to check one by one | 6 | 19.4% |
| Don't know what's new | 5 | 16.1% |
| Other | 2 | 6.5% |

### Counterbalance order

| First prototype | n | % |
|---|---:|---:|
| VibePick (chat) | 21 | 67.7% |
| MoodFlix (filter) | 10 | 32.3% |

---

## §2 Primary outcome — Time-to-first-pick (seconds)

**VibePick** M = 8.87s, Mdn = 1.85s, SD = 19.24
**MoodFlix**  M = 9.94s, Mdn = 1.05s, SD = 25.28

| Statistic | Value |
|---|---|
| Mean difference (VP − MF) | -1.07s (SD = 26.72) |
| Paired t (df = 27) | t = -0.212 |
| p (paired t, raw seconds) | p = 0.834 (ns) |
| Wilcoxon signed-rank p | p = 0.014 (*) |
| Cohen's dz (paired) | -0.040 |
| Log-time paired t | t = 2.145, p = 0.041 (*) |
| Log-time Wilcoxon p | p = 0.004 (**) |
| Cohen's dz (log units) | 0.405 |

**Interpretation.** The raw-seconds distribution is right-skewed (medians 1–2s vs means 9–10s), so the raw paired t-test is non-significant (t = -0.21, p = 0.834). On **log-transformed time**, both paired t (p = 0.041) and Wilcoxon signed-rank (p = 0.0043) indicate VibePick is significantly *slower* in log units, dz = +0.41. The arithmetic mean difference of -1.1s is small in absolute terms.

See `figures/fig1_time_paired_scatter.png` and `figures/fig6_time_distributions.png`.

---

## §3 Secondary outcomes — 1–7 Likert scales (paired t-tests)

| Outcome | VP M (SD) | MF M (SD) | Δ | t | p | sig | dz |
|---|---|---|---:|---:|---:|---|---:|
| Satisfaction | 4.68 (1.22) | 4.71 (0.98) | -0.04 | -0.17 | p = 0.869 | ns | -0.03 |
| Transparency | 5.00 (1.22) | 4.32 (1.02) | +0.68 | 2.33 | p = 0.028 | * | 0.44 |
| Trust        | 4.46 (1.10) | 4.61 (1.13) | -0.14 | -0.64 | p = 0.526 | ns | -0.12 |

**Key finding.** **Transparency** is significantly higher for VibePick (chat-style, with explicit "why I picked this") than MoodFlix (filter UI). Wilcoxon confirms (p = 0.0159). Cohen's dz = +0.44 → small-to-medium effect.

Satisfaction and trust do not differ significantly.

See `figures/fig2_satisfaction_bars.png`, `figures/fig3_transparency_bars.png`, `figures/fig4_trust_bars.png`.

---

## §4 Comparative preference — "If you had to keep just one"

| Choice | n | % |
|---|---:|---:|
| Hard to say | 11 | 35.5% |
| MoodFlix | 11 | 35.5% |
| VibePick | 9 | 29.0% |

Binomial test (VibePick vs MoodFlix, excluding "Hard to say"): **9 / 20** prefer VibePick → p = 0.824 (ns).

See `figures/fig5_comparative_pie.png`.

---

## §5 Order effect

The order balance is **skewed**: 21 used VibePick first, 10 used MoodFlix first. This violates full counterbalancing and is acknowledged as a limitation in §6.

See `figures/fig7_order_imbalance.png`.

---

## §6 Limitations

1. **Order imbalance** (21 vs 10). An order-effect test (mixed-model or carryover-adjusted) is recommended for Phase 2.
2. **Skewed time data** — raw seconds right-skewed (medians ~1–2s vs means ~9–10s); log-transform is the more appropriate scale.
3. **Sample size** — n = 28 pairs reaches ~80% power to detect dz = 0.55 but is underpowered for smaller effects.
4. **Recruitment bias** — primarily Chinese / Western social networks; not stratified to any specific platform user base.
5. **Self-report timing** — participants pasted the time they saw on the final "You picked" screen, which is informal; not instrumented.

---

## §7 Pre-registration alignment (docs/analysis-plan.md)

| Pre-registered question | Outcome | α | Result |
|---|---|---|---|
| H1: VP faster than MF (log-time) | log_t = 2.15, p = 0.041 | .05 | **REJECTED (VP slower on log scale)** |
| H2: VP more transparent | t = 2.33, p = 0.028 | .05 | **SUPPORTED (VP > MF, dz = +0.44)** |
| H3 (exploratory) satisfaction | t = -0.17, p = 0.869 | .05 | Not significant |
| H4 (exploratory) trust | t = -0.64, p = 0.526 | .05 | Not significant |
