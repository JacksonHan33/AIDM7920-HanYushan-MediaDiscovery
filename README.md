# AIDM7920-HanYushan-MediaDiscovery

> COMM7660 / AIDM7920 Individual Project — From Media Evidence to a Working Media Product Prototype
>
> Student PM: **Han Yushan** (GitHub: [@JacksonHan33](https://github.com/JacksonHan33))
> Instructor: **Professor Charles Feng** (GitHub: [@fffchaobu](https://github.com/fffchaobu))

This repository holds the complete evidence for the COMM7660 / AIDM7920 individual project. Phase 1 ends on **October 19, 2026**; Phase 2 ends on **November 19, 2026**. Each phase is also submitted as a short report via Moodle.

---

## Media product (working direction)

- **Direction**: Cross-platform video discovery — a small Web app that helps global video-platform users pick something to watch given their available time and current mood, drawing on a cross-platform availability layer (JustWatch).
- **Two competing concepts compared in Phase 1** (within-subjects design, 30 paired participants):
  - **VibePick** — conversational AI recommendation (chat-style input, AI-written rationale).
  - **MoodFlix** — structured filter recommendation (time-bucket + mood + genre + platform chips, transparent match scoring).
- **Intended audience**: video-platform users aged 15–55 globally who actively stream on Netflix, Disney+, Prime Video, Apple TV+, HBO Max, Hulu, and YouTube.
- **Product name**: finalized at the end of Phase 1 based on the within-subjects pilot.

---

## Submission deadlines

| Phase | Deadline | Channels |
|---|---|---|
| Phase 1 (Media Analytics + Concept Choice) | **October 19, 2026** | GitHub (this repo, tag `phase1-analytics`) + Moodle (short report, identical to Release attachment) |
| Phase 2 (MVP + CI/CD) | **November 19, 2026** | GitHub (this repo, tags `v0.1-working` and `v0.2-submission`) + Moodle (short report, identical to Release attachment) |

Both phase deliverables are submitted **twice** — once to GitHub (complete evidence) and once to Moodle (short report). The Moodle report and the matching GitHub Release attachment are **byte-identical**.

---

## Collaborator

- **Instructor**: Professor Charles Feng — GitHub username `fffchaobu`
- **Repository invitation**: sent at the start of Phase 1 (see `docs/collaborator-invite-status.md` for the screenshot record and current status).
- **Access policy**: instructor access is retained through the end of Phase 2 and any post-grading review period. Do not remove or downgrade the collaborator.

---

## Repository structure

```
README.md                     — this file
docs/                         — plans, decision memos, references
  AIDM7920-HanYushan-WorkPlan-Phase1-2.docx   — Phase 1 working plan (600–800 words, all 9 PDF items)
  decision-memo.md            — Phase 1 → Phase 2 concept choice (filled at end of Phase 1)
  findings.md                 — Phase 1 principal findings (filled at end of Phase 1)
  references.md               — source citations with full bibliographic detail
  collaborator-invite-status.md — record of fffchaobu invitation
data/                         — raw + cleaned data, codebook, source manifest
analysis/                     — executable scripts (with seed), full results, ≥3 figures
  scripts/                    — Python / R analysis scripts
  figures/                    — output figures (PNG / SVG)
  results/                    — CSV / JSON output tables
evaluation/                   — pilot records, user evidence, AI-use logs
product/                      — MVP source, ranking / prompt logic, UI components
tests/                        — automated checks, Playwright scripts
.github/workflows/            — CI/CD: Actions configuration, Playwright runs, deploy
```

Filled-in content under each folder is added as Phase 1 and Phase 2 progress. The PDF Table 8 maps directly to this layout.

---

## Phase 1 route (toward Oct 19)

1. Working plan: see `docs/AIDM7920-HanYushan-WorkPlan-Phase1-2.docx`.
2. Pilot data: 10–20 records validating JustWatch API + time-bucket taxonomy (logged in `data/pilot/`).
3. Frozen analysis plan: pre-registered outcomes and covariates (in `docs/analysis-plan.md`).
4. Data collection: 30 paired participants, within-subjects, counterbalanced order.
5. Analysis: paired comparison (paired t + linear mixed-effects + Wilcoxon signed-rank).
6. Decision: VibePick vs MoodFlix → chosen for Phase 2 MVP, written up in `docs/decision-memo.md`.
7. Release: tag `phase1-analytics` on the final commit; attach the identical Moodle PDF report.

---

## Phase 2 route (toward Nov 19)

1. Build: implement the chosen variant in `product/`.
2. Test: Playwright end-to-end in `tests/`; CI in `.github/workflows/`.
3. Deploy: GitHub Pages (static browser product); deploy logs preserved in `evaluation/`.
4. User evidence: PostHog (or approved local event export) → `evaluation/`.
5. Two numbered GitHub Releases: `v0.1-working` (working prototype) and `v0.2-submission` (assessed build). Phase 1's `phase1-analytics` tag is preserved unchanged.

---

## Reproducibility

- **Python**: 3.11+
- **Required packages**: see `requirements.txt` (added at the start of Phase 1 analysis).
- **Rerun**: every analysis script is deterministic with a fixed seed; rerunning `analysis/scripts/main.py` reproduces all figures and headline numbers.
- **Software versions**: pinned in `requirements.txt` and recorded in `docs/analysis-environment.md`.

## Access requirements

- **JustWatch API**: cross-platform availability metadata. Subject to JustWatch's terms.
- **Survey platform**: Prolific, university mailing lists, or social-media channels (no login-protected third-party data stored in the repo).
- **GitHub Actions**: included for private repositories within GitHub's free tier limits.
- **No restricted content** is stored in this repository (no participant-identifiable records, no DRM media, no paywalled datasets).

---

## Working agreement

- **PM**: Han Yushan (the student) — owns scope, decision, and release.
- **Instructor feedback**: informs the work; it does not replace the PM's verification or release decision.
- **Issues and pull requests** are used to record decisions, agent-output reviews, and instructor feedback.
- **Commit volume is not evidence of quality**; rationale and checks are.

