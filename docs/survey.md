# Phase 1 Participant Survey — VibePick vs MoodFlix

> **Within-subjects design.** Each participant completes both prototypes in counterbalanced order, with a 60-second filler task in between.
> **Target N = 30 paired participants.** Pre-registered in `docs/analysis-plan.md`.
> **Screening:** age 15–55 AND current use of ≥ 1 major video streaming service.

## Participant journey (~15 min total)

```
[A] Consent + screening           1 min
        ↓
[B] Pre-task survey               2 min
        ↓
[C] Prototype 1 (VibePick OR MoodFlix, randomized)
        ↓                            ~5-7 min
[D] Post-prototype-1 questions    2 min
        ↓
[E] Filler task (5-question word puzzle, 60 s)
        ↓
[F] Prototype 2 (the other one)   ~5-7 min
        ↓
[G] Post-prototype-2 questions    2 min
        ↓
[H] Comparative (forced choice + why)  1 min
```

---

## [A] Consent + screening (1 min)

| # | Question | Type | Required |
|---|---|---|---|
| A1 | I am **15–55 years old** and consent to participate in this study. | checkbox | yes |
| A2 | I currently subscribe to or actively use **at least one** major video streaming service (Netflix, Disney+, Prime Video, Apple TV+, HBO Max, Hulu, YouTube, or equivalent). | checkbox | yes |
| A3 | **Participant ID** (assigned by recruiter, e.g. `P7X4K2`) | short text | yes |
| A4 | Today's date (auto-filled) | date | yes |

> **Branch:** if A1 or A2 is unchecked → "Sorry, this study requires both. Thank you for your time." End survey.

---

## [B] Pre-task survey (2 min)

| # | Question | Type | Options |
|---|---|---|---|
| B1 | Age band | radio | 15–24, 25–34, 35–44, 45–55 |
| B2 | Region (country) | dropdown | US, GB, HK, CN, JP, Other (specify) |
| B3 | Which video services do you currently use? (multi-select) | checkbox | Netflix, Disney+, Prime Video, Apple TV+, HBO Max, Hulu, YouTube, Other (specify) |
| B4 | How many hours per week do you typically spend streaming video? | radio | < 2, 2–5, 6–10, 11–20, > 20 |
| B5 | Have you ever used a video recommendation tool (JustWatch, Reelgood, Plex Discover, etc.)? | radio | Yes (which?), No |
| B6 | How comfortable are you with finding something to watch across multiple streaming services? | radio (7-pt) | 1 (very uncomfortable) … 7 (very comfortable) |

---

## [C] Prototype session 1 (auto-logged)

The survey hands the participant a **link to the first prototype** (e.g. `https://<user>.github.io/AIDM7920-HanYushan-MediaDiscovery/prototype/?pid=A3&id=vibepick` or `…&id=moodflix`).

The prototype logs (server-side or via Form auto-fill):
- `pid` — participant ID
- `variant` — vibepick / moodflix
- `order` — 1st or 2nd (carried via URL)
- `prototype_started_at` — timestamp
- `first_pick_at` — timestamp when the first card is clicked
- `picked_title_id` — TMDB movie id picked

**Time to first pick (seconds)** is computed as `first_pick_at - prototype_started_at`. This is one of the **primary outcomes** (pre-registered).

After finishing the prototype, the participant clicks "I'm done — next" and returns to the survey.

---

## [D] Post-prototype-1 survey (2 min)

| # | Question | Type |
|---|---|---|
| D1 | **Satisfaction:** "Overall, how satisfied are you with the recommendation you picked?" | 7-pt Likert (1 = very dissatisfied … 7 = very satisfied) |
| D2 | **Perceived transparency:** "The system clearly explained why it recommended this title." | 7-pt Likert (1 = strongly disagree … 7 = strongly agree) |
| D3 | **Perceived trust:** "I trust this system's recommendations." | 7-pt Likert |
| D4 | "What did you like **most** about this prototype?" | long text (optional) |
| D5 | "What did you find **frustrating or confusing**?" | long text (optional) |

(Questions D1–D5 are repeated identically for Prototype 2 as G1–G5.)

---

## [E] Filler task (1 min)

A 5-question word puzzle (e.g. "How many words can you make from the letters A-P-P-L-E-S-D-A-Y?"). Used to mask the previous prototype's experience and reduce carryover effects.

> **Order assignment is recorded by the survey system** via the `order` URL parameter so we can later run the order-effect robustness check.

---

## [F] Prototype session 2 (auto-logged)

Same instrumentation as [C], with the other variant.

---

## [G] Post-prototype-2 survey (2 min)

Same questions as D1–D5, repeated.

---

## [H] Comparative (1 min)

| # | Question | Type |
|---|---|---|
| H1 | "If you had to keep **just one** of the two prototypes, which would you actually use?" | radio: VibePick / MoodFlix / (refuse to choose) |
| H2 | "Why?" (1–3 sentences) | long text (required if H1 ≠ refuse) |
| H3 | (System check) **Order seen first** | auto: VibePick / MoodFlix |
| H4 | (System check) **Order seen second** | auto |
| H5 | (System check) **Time on each prototype (seconds)** | auto |
| H6 | (System check) **Title picked on each prototype (TMDB id)** | auto |

---

## Data output

Each participant contributes **one row per prototype** in `data/cleaned/observations.csv`:

| pid | order | variant | time_to_first_pick_s | satisfaction | trust | transparency | picked_title_id | like_text | frustrate_text |
|---|---|---|---|---|---|---|---|---|---|
| P7X4K2 | 1 | vibepick | 38.2 | 6 | 5 | 6 | 550988 | "Natural language was easy." | "Couldn't see runtime." |
| P7X4K2 | 2 | moodflix | 22.5 | 5 | 4 | 7 | 1399 | "Match score was clear." | "Too many clicks." |

And **one row per participant** in `data/cleaned/participants.csv` for the pre-survey + comparative.

---

## Implementation notes

- **Form platform:** Google Forms (free) is the fastest to set up; supports all question types above. Each section becomes a "page" with "section break (next page)".
- **Prototype URL delivery:** since each prototype needs the participant ID and order embedded in the URL, a single Google Form section can't handle the redirect cleanly. Two practical options:
  1. **Two Google Forms** (one per prototype post-survey), with the prototype URL shown as a "continue" link between forms.
  2. **One custom HTML form** that embeds the prototypes inline and logs data via a small backend (Cloudflare Worker, GitHub Pages + formspree, etc.).
- **Time measurement:** JavaScript timestamp on the prototype page (`performance.now()` when the page renders vs. when the first card is clicked) is the most accurate. Google Form timestamps are page-level only, so we lose per-prototype timing precision if we go pure-Forms.
- **Recommended for Phase 1:** **option 2**, a single small web app that hosts both prototypes and the survey. We'll design it after this survey doc is approved.

---

## Pre-registration note

All questions above, all response scales, and all outcomes are **frozen** in this document. Any post-data-collection change to the survey must be:
1. Recorded in `docs/analysis-plan.md` §10 Amendments log
2. Labeled exploratory
3. Justified in the Phase 1 report


---

## ADDENDUM (2026-10-18) — 4 market-validation questions

Per teacher feedback, the following questions should be inserted into the live Google Form **after the existing Q3 (Prolific ID)**. These questions collect the demand-side evidence referenced in `docs/market-analysis.md`.

**Insert at position Q1a (after Q1 Prolific ID):**

| Q# | Question | Type | Options |
|---|---|---|---|
| Q1a | How often do you switch between streaming services to find something to watch? | Multiple choice (Required) | `Daily / Weekly / Monthly / Rarely` |

**Insert at position Q3a/b/c (after Q3 Have you used a video recommendation tool before?):**

| Q# | Question | Type | Options |
|---|---|---|---|
| Q3a | In the past month, how many times did you want to watch something but couldn't easily find WHERE it was streaming? | Multiple choice (Required) | `0 / 1-2 / 3-5 / 6+` |
| Q3b | What's your biggest pain point when looking for something to watch? (multi-select) | Checkboxes (Required) | `Don't know which service has the movie / Too many services to check one by one / Recommendations are bad / Don't know what's new / Other` |
| Q3c | How much time do you typically spend searching for something to watch? | Multiple choice (Required) | `< 5 min / 5-15 min / 15-30 min / > 30 min` |
