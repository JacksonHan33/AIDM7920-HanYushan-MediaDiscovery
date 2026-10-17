# Phase 1 — Frozen Analysis Plan

> **This document is the pre-registered analysis plan for COMM7660 / AIDM7920 Phase 1. It is frozen before substantive data collection begins. Any change after the freeze is logged in §10 Amendments Log with reason and date.**

| | |
|---|---|
| **Author** | Han Yushan (GitHub: @JacksonHan33) |
| **Plan frozen** | October 13, 2026 (before participant recruitment) |
| **Data cutoff** | October 19, 2026 (Phase 1 deadline) |
| **Phase 1 deadline** | October 19, 2026 |
| **Repository** | github.com/JacksonHan33/AIDM7920-HanYushan-MediaDiscovery |
| **Plan version** | v1.0 |

---

## 1. Research question

For the "find me something to watch in my situation" task — given a defined time window, a mood, and the platforms the user already subscribes to — **do users prefer a conversational AI interface (VibePick) or a structured filter interface (MoodFlix), and what predicts that preference?**

## 2. Competing concepts (frozen)

Both VibePick and MoodFlix use the same cross-platform availability data source (TMDB watch providers) and serve the same user need. They differ only in the interaction paradigm.

### 2.1 VibePick (Concept 1, conversational AI)
- **Input:** a single chat-style text box accepting natural-language requests such as "I have 45 minutes, want something funny and light".
- **Output:** three picks in priority order, each with title, poster, runtime, age rating, available platforms in the user's region (via TMDB), and a one-sentence rationale written by the LLM.
- **Backend:** LLM API call constrained to call TMDB availability and a curated catalog; tool-use constraint prevents hallucinated titles.

### 2.2 MoodFlix (Concept 2, structured filter)
- **Input:** a multi-step form — time bucket (3 chips: <30, 30–90, >90 min), mood (5 tags), genre (multi-select), platform (multi-select), with optional language and year filters.
- **Output:** a ranked list of up to 20 titles with poster, runtime, age rating, available platforms, a transparent match score, and an explicit breakdown of why each title matched.
- **Backend:** deterministic ranking over TMDB availability plus a curated catalog; match score = weighted sum of attribute overlap, calibrated by recent popularity.

## 3. Design

**Within-subjects, counterbalanced, paired comparison.** Each participant completes both prototypes.

| | |
|---|---|
| **Order randomization** | 1:1 (VibePick → MoodFlix vs MoodFlix → VibePick), stratified by age band |
| **Filler task between sessions** | A 60-second unrelated word puzzle (5 questions) to mask the previous experience |
| **Per-participant total time** | ~15 min (consent + pre-survey + 2 prototypes × 6 min + filler + post-survey) |

### 3.1 Why within-subjects (not between-subjects)
1. **Statistical power with fewer participants.** 30 paired participants deliver the same power as ~60–80 participants in a between-subjects design. Phase 1 has a 7-day collection window.
2. **Individual-difference noise is absorbed.** Each person is their own control; mood, platform familiarity, and personality cannot bias the comparison.
3. **Direct preference signal.** After the second prototype, each participant picks "which one would you actually use?" — a stronger outcome than comparing two group averages.

## 4. Sample

| | |
|---|---|
| **Population** | Global video-platform users aged 15–55 |
| **Sampling frame** | Online recruitment (Prolific, university mailing lists, social-media channels) + screening for current use of ≥1 major video platform |
| **Target N** | 30 valid paired participants (≈ 60 paired observations) |
| **Stratification** | By age band (15–24, 25–34, 35–44, 45–55) and region where feasible |
| **Screening** | Must confirm age 15–55 AND currently use ≥1 major video platform (Netflix, Disney+, Prime Video, Apple TV+, HBO Max, Hulu, YouTube) |
| **Exclusion** | Incomplete responses (did not complete BOTH prototypes); < 5 s response time on either task (likely random) |

## 5. Outcomes (pre-registered)

### 5.1 Primary
- **Time to first pick** (continuous, in seconds, log-transformed before analysis) — measured from first render of the recommendation list to the first click on a title.
- **Satisfaction** (ordinal, 7-point Likert) — "How satisfied are you with the recommendation you picked?" asked immediately after each pick.

### 5.2 Secondary
- **Perceived transparency** (7-point Likert) — "The system clearly explained why it recommended this title."
- **Perceived trust** (7-point Likert) — "I trust this system's recommendations."
- **Comparative preference** (forced choice) — "If you had to keep just one, which would you actually use?" asked after the second prototype.

### 5.3 Open-ended
- "Why?" (1–3 sentences explaining the comparative preference)

## 6. Predictors and covariates

| Variable | Type | When collected | Role |
|---|---|---|---|
| Assigned version order (AB vs BA) | binary | post-survey | order-effect control |
| Age band (15–24, 25–34, 35–44, 45–55) | categorical | pre-survey | covariate |
| Region | categorical | pre-survey | covariate + subgroup |
| Weekly video-platform hours | continuous | pre-survey | covariate |
| Prior use of recommendation tools (JustWatch, Reelgood, etc.) | ordinal | pre-survey | covariate |

## 7. Statistical model (frozen)

### 7.1 Primary
- **Time to first pick:** paired t-test on log-transformed time, confirmed with a linear mixed-effects model with participant as a random effect and `version`, `order`, `version × order` as fixed effects.
- **Satisfaction (ordinal):** Wilcoxon signed-rank test, confirmed with a paired proportional-odds model.

### 7.2 Secondary
- **Perceived transparency / trust (ordinal):** same as satisfaction (paired models).
- **Comparative preference (binary):** exact binomial test against H₀: p = 0.5.

### 7.3 Effect size reporting
- Continuous: Cohen's d_z (paired) with 95% CI.
- Ordinal: rank-biserial r with 95% CI.
- Binary: risk difference with 95% CI.

### 7.4 Robustness checks
- Sensitivity to outliers: drop top/bottom 1% of time.
- Per-region subgroup: re-estimate within each region with ≥5 participants.
- Order-effect test: does `order` predict satisfaction / time independent of `version`?
- Signed-rank as an alternative to paired t on log(time).
- Ordered logit alternative to proportional-odds.

## 8. Reproducibility

- **Python:** 3.9.x (pinned in `requirements.txt`)
- **Analysis script:** `analysis/scripts/main.py` (added when data collection begins)
- **Random seed:** 42 (frozen; any seed-dependent step is logged)
- **Rerun:** `python3 analysis/scripts/main.py` reproduces all figures and headline numbers
- **Data inputs:** `data/cleaned/participants.csv` (per-participant rows) and `data/cleaned/observations.csv` (per-prototype rows)
- **Outputs:** `analysis/figures/*.png` and `analysis/results/*.csv`

## 9. Decision rule

- Choose the variant with the better primary-outcome effect, **only if**:
  - effect size in the expected direction on both time-to-first-pick and satisfaction, AND
  - the 95% CI on the satisfaction difference excludes zero, AND
  - the order-effect check is non-significant (or explained).
- The chosen variant is written up in `docs/decision-memo.md` at the end of Phase 1.
- The losing variant's code and rationale are retained in the repository for review.

## 10. Amendments log

Every change after the freeze is logged here. Outcome-informed changes are labeled exploratory.

| Date | Section | Change | Reason | Label |
|---|---|---|---|---|
| — | — | (no amendments yet) | — | — |

---

## 11. Approvals

| Role | Name | Date |
|---|---|---|
| Author / PM | Han Yushan | 2026-10-13 |
| (Instructor consulted if needed) | Prof. Charles Feng (@fffchaobu) | TBD |


---

## 11. Market analysis layer (added 2026-10-18)

Per teacher feedback in class on 2026-10-16, Phase 1 must also include a **media analytics** layer that justifies the product direction before the UX comparison. The full market analysis is in `docs/market-analysis.md`, with 5 real academic sources + 1 industry source in `docs/references.md`.

Key findings the market analysis establishes (so the UX study below is justified):

1. **Supply-side fragmentation** — across 189 popular movies, the median has 2-3 distinct streaming providers (Adomavicius & Tuzhilin 2005; Hennig-Thurau et al. 2006).
2. **Demand-side pain** — 157 Google Play reviews of cross-platform video apps show the dominant complaint is "where to watch" (Bauer & Schedl 2019; Pu, Chen & Hu 2011).
3. **Search-trend signal** — Google Trends shows "what to watch" and "JustWatch" queries are growing (industry context).
4. **Industry validation** — JustWatch (40M MAU), Reelgood, TV Time already serve this market (Gomez-Uribe & Hunt 2015 industry framing).

The pre-registered UX study below remains unchanged; this market layer sits above it as the "is this worth doing?" justification.
