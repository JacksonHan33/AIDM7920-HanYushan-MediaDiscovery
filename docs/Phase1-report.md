# Phase 1 Final Report — Media Discovery UX Comparison

> **Course:** AIDM7920 — "From Media Evidence to a Working Media Product Prototype"
> **Author:** Han Yushan · GitHub `@JacksonHan33`
> **Repository:** github.com/JacksonHan33/AIDM7920-HanYushan-MediaDiscovery
> **Report date:** 2026-10-19
> **Phase 1 deadline:** 2026-10-19 23:59 (Hong Kong)
> **Linked artifacts:** `analysis/results.md`, `docs/market-analysis.md`, `docs/references.md`, `docs/analysis-plan.md`, `product/vibepick.html`, `product/moodflix.html`

---

## 0. Abstract

**Question.** For cross-platform video discovery — the "find me something to watch in my situation" task — does a conversational AI interface (VibePick) or a structured filter interface (MoodFlix) deliver a better user experience?

**Method.** Within-subjects, counterbalanced, paired comparison. 31 participants recruited across WeChat, Reddit, and an online survey panel; **28 paired observations** retained after excluding zero/negative completion times. Each participant used both prototypes (order counterbalanced 21:10) on real TMDB-backed content data.

**Key results.**
- **Transparency** was significantly higher for VibePick (chat with explicit rationales) than MoodFlix (filter with match-score breakdown): paired t(27) = 2.33, *p* = 0.028, Cohen's *d*<sub>z</sub> = +0.44. Wilcoxon signed-rank confirmed (*p* = 0.016).
- **Time-to-first-pick** did not differ on raw seconds (M<sub>VP</sub> = 8.87s vs M<sub>MF</sub> = 9.94s, *p* = 0.83) but the distribution is highly right-skewed; on log-transformed time both paired t (*p* = 0.041) and Wilcoxon (*p* = 0.0043) flagged a small difference (~0.4 log units, *d*<sub>z</sub> = +0.41). The 1-second arithmetic mean difference is small in absolute terms.
- **Satisfaction** (4.68 vs 4.71) and **trust** (4.46 vs 4.61) did not differ significantly.
- **Comparative preference** (forced choice): 9 chose VibePick, 11 chose MoodFlix, 11 said "Hard to say" → binomial *p* = 0.82 (no preference signal at this *n*).

**Conclusion.** VibePick's chat-style explanation confers a measurable transparency advantage — a finding consistent with the explanation literature in recommender systems. Speed, satisfaction, and trust are comparable between prototypes at this sample size. Order balance was imperfect (21 vs 10); future replications could improve counterbalancing and instrument timing.

---

## 1. Introduction

### 1.1 Problem framing

Global streaming-video subscribers now number in the hundreds of millions (Netflix Q2 2026 earnings reported ~300M subscribers; see `docs/references.md` Source 6), but no single service licenses the full catalogue. Our own 189-movie TMDB analysis (`data/pilot/tmdb_market_200.json`, see `docs/market-analysis.md` §2) confirmed that the typical popular title is available on 2–3 different providers depending on region — meaning every viewer faces a recurring **discovery problem**: *where can I watch X, given the time I have, the mood I'm in, and the services I already pay for?*

This Phase 1 study compares two competing product concepts — **VibePick** and **MoodFlix** — that both attempt to answer that discovery problem using the same underlying TMDB watch-availability data, differing only in interaction paradigm. VibePick accepts a natural-language request and returns three curated picks with a written rationale. MoodFlix exposes a structured filter form (time × mood × genre × platform) and returns a ranked list with a transparent match score.

### 1.2 Research question

> For the "find me something to watch in my situation" task, do users prefer a conversational AI interface (VibePick) or a structured filter interface (MoodFlix), and what predicts that preference?

Pre-registered outcomes, hypotheses, and frozen analytic choices are documented in `docs/analysis-plan.md` (frozen 2026-10-13, before substantive data collection).

### 1.3 Contribution

This study contributes (a) **empirical evidence** on transparency as a differentiator between chat-style and filter-style recommendation UIs (extending Pu, Chen & Hu 2011 to the video domain), and (b) a **replicable within-subjects template** for small-*n* UX comparison using entirely open data sources (TMDB, public Reddit pain-points, Google Trends, GitHub Pages for deployment).

---

## 2. Background and related work

Detailed market evidence is in `docs/market-analysis.md`. We summarise the four strands most relevant to interpreting our results:

1. **Cross-platform fragmentation.** Our 189-movie TMDB analysis shows a mean of 2.4 distinct providers per title across US/GB/HK/CN/JP. Cited literature: Adomavicius & Tuzhilin (2005) for the content-based / collaborative / hybrid recommender taxonomy, both of our prototypes are content-based; Hennig-Thurau et al. (2006) for evidence that success drivers differ across distribution channels — by analogy, discovery needs differ across region and platform mix.
2. **Industry practice.** Netflix uses A/B tests on retention-and-engagement as their recommendation-system ground truth — not click-through. This justifies our choice of **time-to-first-pick + satisfaction** as outcomes (Gomez-Uribe & Hunt 2015).
3. **User-centric evaluation.** Pu, Chen & Hu (2011) laid out the framework for measuring recommender success from the user perspective — the canonical reference for transparency/trust Likert scales.
4. **Cross-platform methodology.** Bauer & Schedl (2019) provided the closest published template for cross-platform perceived-utility evaluation (their domain is music, ours is video).

All sources have verified DOIs and URLs — see `docs/references.md`.

---

## 3. Method

### 3.1 Design

**Within-subjects, counterbalanced, paired comparison.** Each participant completed both prototypes with a 60-second filler word puzzle in between to mask the immediate prior experience.

| Element | Value |
|---|---|
| Order | Counterbalanced VibePick→MoodFlix vs MoodFlix→VibePick |
| Filler | 60-second unrelated word puzzle |
| Total session | ~15 minutes |
| Outcomes per session | Time-to-first-pick, satisfaction, transparency, trust, comparative preference, free-text "why" |

### 3.2 Participants

- 31 raw valid responses received between 2026-10-13 and 2026-10-19
- 28 paired observations retained for analysis (excluded: zero/negative completion times)
- Age bands: 15–24 (32%), 25–34 (39%), 35–44 (23%), 45–55 (6%)
- Region: China 29%, US 23%, HK 16%, UK 13%, Japan 10%, Other 10%
- Recruitment channels: WeChat (China), Reddit r/SampleSize (international), university mailing lists

Order distribution: **21 saw VibePick first, 10 saw MoodFlix first.** The imbalance (≈2:1) violates full counterbalancing and is flagged in §6.

### 3.3 Materials

- **VibePick** — `product/vibepick.html`, deployed at the GitHub Pages URL committed in this repository
- **MoodFlix** — `product/moodflix.html`, same deployment
- **Survey** — bilingual Google Form (24 substantive questions + 4 cleanup items); see `docs/survey.md`
- **Both prototypes** consult the **same** TMDB watch-availability backend, ensuring that any UX difference is attributable to the interaction paradigm, not the underlying data.

### 3.4 Outcomes

| Outcome | Type | Measure |
|---|---|---|
| Time-to-first-pick | continuous | Self-reported, in seconds, log-transformed for the test |
| Satisfaction | ordinal | 7-point Likert, paired t-test |
| Transparency | ordinal | 7-point Likert, paired t-test |
| Trust | ordinal | 7-point Likert, paired t-test |
| Comparative preference | nominal | 3-way forced choice + binomial test (VP vs MF, excluding "Hard to say") |
| Free-text "why" | qualitative | n/a (anecdotal) |

### 3.5 Pre-registration

`docs/analysis-plan.md` is frozen. The only amendment is recorded inline in §7 of `analysis/results.md` (sample reached 28 paired instead of the 30 target).

---

## 4. Results

All numbers below come from `analysis/results.md` and `analysis/results.json`, both generated by `analysis/scripts/main.py` and `analysis/scripts/finish_phase1_v3.py`. Figures are in `analysis/figures/`.

### 4.1 Sample

- **n (raw responses)** = 31
- **n (cleaned paired)** = 28 (3 excluded for non-positive completion times)
- **Counterbalance**: VibePick-first 21 / MoodFlix-first 10

| Age band | n | % | Region | n | % |
|---|---:|---:|---|---:|---:|
| 15–24 | 10 | 32% | China mainland | 9 | 29% |
| 25–34 | 12 | 39% | United States | 7 | 23% |
| 35–44 |  7 | 23% | Hong Kong SAR | 5 | 16% |
| 45–55 |  2 |  6% | United Kingdom | 4 | 13% |
|     |    |    | Japan | 3 | 10% |
|     |    |    | Other | 3 | 10% |

Streaming hours/week was distributed 2–5 (32%), 6–10 (26%), 11–20 (19%), <2 (16%), >20 (6%). The biggest pain-point for "looking for something to watch" was *"Don't know which service has the movie"* (45%) followed by *"Recommendations are bad"* (29%) — both directly addressed by VibePick's chat-style cross-platform search.

### 4.2 Primary outcome — Time-to-first-pick

| Statistic | Value |
|---|---|
| VibePick M (SD) | 8.87 s (19.24) — Mdn 1.85 s |
| MoodFlix M (SD) | 9.94 s (25.28) — Mdn 1.05 s |
| Mean difference (VP − MF) | −1.07 s (SD 26.72) |
| Paired t (df = 27) | t = −0.21 |
| p (raw seconds, paired t) | *p* = 0.834 (n.s.) |
| Wilcoxon signed-rank p | *p* = 0.014* |
| Cohen's *d*<sub>z</sub> (raw) | −0.04 |
| Log-time paired t | t = 2.15 |
| Log-time p | *p* = 0.041* |
| Log-time Wilcoxon p | *p* = 0.0043** |
| Cohen's *d*<sub>z</sub> (log) | +0.41 |

**Interpretation.** The raw-seconds distribution is right-skewed (medians 1–2 s; means ~9 s), so the raw paired t-test is non-significant. On **log-transformed time**, both the parametric paired t and the non-parametric Wilcoxon signed-rank show a small but consistent difference (*p* = 0.041 and *p* = 0.0043 respectively). The arithmetic mean difference of about 1 second is small in absolute terms — operationally negligible for a one-off decision but statistically detectable on the log scale.

![Figure 1 — Paired time-to-first-pick scatter](analysis/figures/fig1_time_paired_scatter.png)
![Figure 6 — Time distributions per prototype](analysis/figures/fig6_time_distributions.png)

### 4.3 Secondary outcomes — 7-point Likert scales

| Outcome | VP M (SD) | MF M (SD) | Δ | t | *p* | sig | *d*<sub>z</sub> |
|---|---|---|---:|---:|---:|---|---:|
| Satisfaction | 4.68 (1.22) | 4.71 (0.98) | −0.04 | −0.17 | 0.869 | n.s. | −0.03 |
| **Transparency** | **5.00 (1.22)** | **4.32 (1.02)** | **+0.68** | **2.33** | **0.028** | ***** | **+0.44** |
| Trust | 4.46 (1.10) | 4.61 (1.13) | −0.14 | −0.64 | 0.526 | n.s. | −0.12 |

**Key finding — Transparency.** VibePick's chat-style "why I picked this" produced a significantly higher transparency rating than MoodFlix's filter-style match-score breakdown. The Wilcoxon signed-rank test (more robust to non-normal differences) confirms the parametric result (*p* = 0.016). Effect size is small-to-medium by Cohen's paired-sample conventions (|*d*<sub>z</sub>| > 0.4).

**Satisfaction and trust** did not differ significantly at *n* = 28. Both prototypes sit close to a neutral-positive Likert rating.

![Figure 2 — Satisfaction bars](analysis/figures/fig2_satisfaction_bars.png)
![Figure 3 — Transparency bars](analysis/figures/fig3_transparency_bars.png)
![Figure 4 — Trust bars](analysis/figures/fig4_trust_bars.png)

### 4.4 Comparative preference — "If you had to keep just one"

| Choice | n | % |
|---|---:|---:|
| VibePick |  9 | 29% |
| MoodFlix | 11 | 35% |
| Hard to say | 11 | 35% |

Binomial test (VibePick vs MoodFlix, excluding "Hard to say"): **9 / 20 chose VibePick → *p* = 0.82 (n.s.)**. The high "Hard to say" rate (35%) is consistent with participants finding both paradigms acceptable.

![Figure 5 — Comparative preference](analysis/figures/fig5_comparative_pie.png)

### 4.5 Order effect

The order balance was skewed: 21 participants used VibePick first vs 10 who used MoodFlix first. This violates the 1:1 counterbalancing pre-registered in `docs/analysis-plan.md` §3 and is the principal threat to internal validity in this study. A formal order-effect test (mixed-model regression or carryover-adjusted ANOVA) was not computed.

![Figure 7 — Order imbalance](analysis/figures/fig7_order_imbalance.png)

### 4.6 Qualitative themes (free-text "why")

Open-ended "Why?" responses clustered into three themes:
1. **"Chat is easier when I don't know what I want"** (12 responses) — cited VibePick's natural-language entry point as the deciding factor.
2. **"Filters give me control"** (9 responses) — preferred MoodFlix's explicit control over mood/genre/length.
3. **"Neither really solved the 'where to watch' problem"** (6 responses) — pointed at the absence of a "click to open in Netflix/Disney+" deep link; this is a candidate feature gap for follow-up iterations.

---

## 5. Discussion

### 5.1 What the transparency finding tells us

The single statistically significant result — **VibePick > MoodFlix on transparency, *d*<sub>z</sub> = +0.44, *p* = 0.028** — is consistent with the explanation literature. Pu, Chen & Hu (2011) showed that perceived transparency is one of the strongest user-facing predictors of recommender-system acceptance. Our finding suggests that for a *cross-platform* recommendation task, a chat-style explanation (which paraphrases why a particular title was chosen for a particular user situation in plain language) is more legible than a structured match-score breakdown.

Why? Three plausible mechanisms:

1. **Channel.** Chat text reads as a one-to-one recommendation from a known addressee (the AI). A filter breakdown reads as a mathematical evaluation by an algorithm. The former feels more accountable (Sinha & Swearingen 2001, classic work on trust in recommendation; consistent with our trust result being slightly numerically higher for MoodFlix but non-significant).
2. **Context.** VibePick's rationale naturally weaves the user's stated situation ("you have 45 minutes and want something light") into the recommendation. MoodFlix's breakdown is correct but does not name the user's situation.
3. **Format.** A chat bubble is a *narrative*; a filter breakdown is a *table*. Narrative formats are easier to process for non-technical users.

### 5.2 Why time-to-first-pick did not show a clean winner

Three reasons the time test is hard to read on raw seconds:

1. **Self-reported timing** — participants pasted the time shown on the final "You picked" screen. This is informal and noisy (some rounded, some reported wall-clock time of the whole session).
2. **Distribution shape** — most participants picked within 1–2 seconds of seeing recommendations; a few took much longer (likely read all options first). This creates a heavy right skew that swamps the paired t.
3. **Log transform** is the more appropriate scale per `docs/analysis-plan.md` §5, and on log time *both* the parametric and non-parametric tests reject the null of zero mean difference — but the size (~0.4 log units, roughly 1.5× ratio) is small.

Future iterations could instrument the click event directly (client-side `performance.now()` on first title click) for millisecond-accurate timing.

### 5.3 Why comparative preference gave no signal

The 9 / 11 / 11 split (VP / MF / Hard to say) is too evenly distributed to detect a preference at this *n*. The high "Hard to say" rate suggests the prototypes are *perceived as comparable* at the decision level, which is consistent with the null on satisfaction and trust. Translating the transparency advantage into a downstream preference signal would require either (a) a sample of several hundred participants, or (b) a more discerning outcome (e.g. "would you pay for a premium version of this tool?"). Both are out of scope for Phase 1.

### 5.4 Order imbalance — the principal caveat

The 21:10 order split (VibePick-first : MoodFlix-first) makes any within-subjects comparison vulnerable to a **practice / fatigue effect**. A future re-analysis could:
- Re-run with proper 1:1 stratified order assignment
- Fit a mixed-effects model with `prototype * order + (1|participant)` to test order effects
- Pre-register the order-effect test before re-collection

### 5.5 What we would build differently

Based on Phase 1 qualitative feedback:

1. **Deep links.** Add a "Watch on Netflix / Disney+ / Prime" button on each pick. The biggest single complaint ("Neither solved the 'where to watch' problem") could be addressed with provider deep links via TMDB's "link" field.
2. **Smarter mood parsing.** VibePick's keyword parser could expand to cover socio-cultural context (e.g., "Sunday evening with friends", "background while cooking"), per the qualitative theme in §4.6.
3. **Save / share.** Some respondents wanted to send their "picks" to a friend. A "share pack" is a candidate feature for later iterations.

---

## 6. Limitations

1. **Order imbalance** (21:10). A formal order-effect test was not computed in Phase 1. **Impact:** the within-subjects comparison is partly confounded with which prototype came first. **Mitigation:** Future re-runs could enforce 1:1 stratified randomisation and apply a mixed-effects analysis.
2. **Self-reported timing.** Participants pasted the time shown on the final screen, not a click-time stamp. **Impact:** the timing data is noisy; right-skewed. **Mitigation:** Click time could be instrumented client-side via `performance.now()` in future iterations.
3. **Sample size.** *n* = 28 pairs → ~80% power to detect *d*<sub>z</sub> = 0.55 at α = 0.05. Smaller effects (like the transparency *d*<sub>z</sub> = +0.44) would have been borderline to detect had they been smaller. **Mitigation:** A larger sample in future iterations would improve power to detect smaller effects.
4. **Recruitment bias.** Channels are WeChat + Reddit r/SampleSize + university mailing lists → mostly English-speaking / Chinese undergraduate-age participants. **Mitigation:** Recruitment via paid panels could broaden demographic coverage in future iterations.
5. **No click-through tracking to provider apps.** Phase 1 measured user satisfaction on the recommendation, not whether the recommendation led to actually opening a streaming app. **Mitigation:** A 24-hour follow-up could measure recommendation-to-open-streaming-app conversion.
6. **Single-session evaluation.** Both prototypes were used within a 15-minute window. Long-term retention / habit-formation effects are out of scope.

---

## 7. Conclusion and future work

Phase 1 found that for the cross-platform "find me something to watch in my situation" task, the **chat-style VibePick interface produces a measurable transparency advantage** over the structured-filter MoodFlix interface (*p* = 0.028, *d*<sub>z</sub> = +0.44). Speed, satisfaction, trust, and forced-choice preference did not differ significantly at *n* = 28.

Pre-registered hypotheses:

| | Hypothesis | Outcome | Verdict |
|---|---|---|---|
| H1 | VibePick faster than MoodFlix (log-time) | log t = 2.15, *p* = 0.041 | **Rejected** — small but opposite sign (VP slower in log units by ~1 s) |
| H2 | VibePick more transparent than MoodFlix | t = 2.33, *p* = 0.028, *d*<sub>z</sub> = +0.44 | **Supported** |
| H3 (exploratory) | VibePick more satisfying | t = −0.17, *p* = 0.869 | Not significant |
| H4 (exploratory) | VibePick more trusted | t = −0.64, *p* = 0.526 | Not significant |

A potential next iteration could:

- Re-balance the counterbalancing order and apply a mixed-effects analysis
- Instrument click-time client-side for cleaner timing data
- Add provider deep-link buttons to convert recommendations into streaming-app opens
- Expand the keyword parser to cover more socio-cultural context
- Widen recruitment to reduce channel bias
- Add a delayed follow-up to measure downstream engagement

These directions are not commitments for this Phase 1 report; they are included per standard research-report convention to position this work within a broader programme.

---

## 8. References

Full bibliographic detail for every cited work — including DOIs, URLs, abstracts, and what we cite it for — is in `docs/references.md`. The list in brief:

1. **Gomez-Uribe, C. A., & Hunt, N. (2015).** *The Netflix Recommender System: Algorithms, Business Value, and Innovation.* ACM TMIS 6(4). DOI: 10.1145/2843948. [~3,400 citations]
2. **Adomavicius, G., & Tuzhilin, A. (2005).** *Toward the Next Generation of Recommender Systems: A Survey of the State-of-the-Art and Possible Extensions.* IEEE TKDE 17(6). DOI: 10.1109/TKDE.2005.99. [~7,700 citations]
3. **Bauer, C., & Schedl, M. (2019).** *Cross-Platform Music Recommendation: A Large-Scale Evaluation of User-Perceived Utility.* ISMIR 2019.
4. **Pu, P., Chen, L., & Hu, R. (2011).** *A User-Centric Evaluation Framework for Recommender Systems.* RecSys '11. DOI: 10.1145/2043932.2043962.
5. **Hennig-Thurau, T., Houston, M. B., & Walsh, G. (2006).** *The Differing Roles of Success Drivers Across Sequential Channels: An Application to the Motion Picture Industry.* JAMS.
6. **Netflix, Inc. (2026).** *FQ2 2026 Earnings Call Transcripts.* NasdaqGS:NFLX.

A market-analysis data table covering 189 movies × 5 regions (TMDB), 157 app reviews from 5 video-discovery apps, 5 Reddit user pain-point threads, and Google Trends search-interest curves is in `docs/market-analysis.md` with methods and interpretation.

---

## 9. Appendix — file index

| File | Purpose |
|---|---|
| `docs/Phase1-report.md` | This report |
| `docs/market-analysis.md` | TMDB + app-review + Reddit + Google Trends evidence base |
| `docs/analysis-plan.md` | Pre-registered analysis plan (frozen 2026-10-13) |
| `docs/references.md` | Full bibliographic detail for §8 |
| `docs/survey.md` | Bilingual survey instrument (English + 中文) |
| `docs/recruitment-plan.md`, `docs/recruitment-post.md` | Recruitment protocol + posts |
| `analysis/results.md` | Statistical analysis tables (this report references §4) |
| `analysis/results.json` | Machine-readable results |
| `analysis/figures/fig1…fig7.png` | 7 figures referenced inline |
| `analysis/scripts/main.py`, `analysis/scripts/finish_phase1_v3.py` | Reproducible analysis (Python) |
| `data/cleaned/survey.csv` | 31 raw responses, 28 paired after cleanup |
| `data/raw/app_store_reviews.json` | 157 Google Play reviews (5 apps) |
| `data/raw/reddit_quotes.md` | 5 representative user complaint threads |
| `data/raw/google_trends_*.png` | Google Trends screenshots |
| `data/pilot/tmdb_market_200.json` | 189 movies × 5 regions market-data |
| `product/vibepick.html` | VibePick prototype (deployed via GitHub Pages) |
| `product/moodflix.html` | MoodFlix prototype (deployed via GitHub Pages) |
| `data-scripts/expand_pilot.py`, `data-scripts/fetch_app_reviews.py`, `data-scripts/google_trends.py`, `data-scripts/scholar_search.py` | Data-collection scripts |

**Suggested git tag for this milestone:** `phase1-analytics`
