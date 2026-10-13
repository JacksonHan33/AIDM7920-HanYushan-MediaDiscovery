# Phase 1 Recruitment Plan

> **Target:** 30 valid paired participants (within-subjects design, both prototypes).
> **Period:** Oct 14 (Wed) → Oct 17 (Sat), 4 days.
> **Total test time per participant:** ~15 min.
> **Total testing time:** ~7.5 hours spread over 4 days.

---

## 1. Channel mix

| Channel | Cost | Speed | Typical yield | Use for |
|---|---|---|---|---|
| **Prolific** | ~$1.5 / participant | 24 h | 30 in 1 day if paid | primary, after the pilot |
| **University mailing list / class WeChat group** | free | 1–3 days | 5–15 per day | first wave (Oct 14) |
| **Personal network (friends, family, classmates)** | free | hours | 3–10 per day | fastest first batch |
| **WeChat Moments / Xiaohongshu** | free | 1–3 days | variable | bonus |

> **Strategy:** **personal network first** (fastest, 1 day) → **university list** (Oct 15) → **Prolific top-up** (Oct 16–17 if under 25).

---

## 2. Screening rules (in recruitment post)

The recruitment post **must** say:

> "I'm a student doing a 15-minute academic user study comparing two ways to find something to watch. You need to be **15–55 years old** and **currently use at least one major video streaming service** (Netflix, Disney+, Prime Video, Apple TV+, HBO Max, Hulu, YouTube, or similar). You'll get a small thank-you (¥10 / US$1.5 voucher) for your time."

This pre-filters so the actual survey's A1/A2 gates catch no one.

---

## 3. Sample size & quotas

| Dimension | Target | Why |
|---|---|---|
| Total N | **30 paired** | matches `docs/analysis-plan.md` |
| Age bands | roughly even split between 15–24, 25–34, 35–44, 45–55 (≥ 5 each if possible) | covariate stratification |
| Region | open, record in pre-survey | covariate |
| Order (AB vs BA) | 15 / 15 (auto-balanced by random assignment) | counterbalance |

If a quota can't be met (e.g., not enough 45–55), we don't enforce hard quotas — the analysis plan allows it as a covariate.

---

## 4. Recruitment posts (templates)

### 4.1 WeChat / class group post (Chinese)
> 【15 分钟学术调研招募】
> 同学你好，我是 COMM7660 的同学，正在做一个比较两种"找片看"方式的学术研究。
> 需要你用 15 分钟，分别试用两个找片工具并填一份简短问卷。
> 要求：15-55 岁、目前至少用一个视频平台（Netflix / Disney+ / 优酷 / B 站等）。
> 报酬：¥10 红包，完成即发。
> 链接：[survey link]
> 谢谢！

### 4.2 Prolific post (English)
> Title: 15-min user study on two ways to find something to watch
> Description: We are researchers comparing two prototypes that help you pick a movie or show to watch given your time and mood. You'll use both prototypes (~10 min total) and answer a short survey (~5 min). You must be 18+ (Prolific policy) and currently use at least one major streaming service. Reward: $1.50.
> Estimated time: 15 minutes
> [consent + screening form URL]

### 4.3 Personal ask (DM/WeChat)
> Hey — quick favor? I'm running a 15-min user study for my class, comparing two ways to pick what to watch on Netflix etc. You only need to be a video-streaming user. ¥10 / $1.5 thank-you. Link: [URL]. Thanks so much!

---

## 5. Daily schedule (Oct 14–17)

| Day | Date | Action | Target |
|---|---|---|---|
| 1 | Wed Oct 14 | Send recruitment post to personal network + 1 class group; **accept first 8–10** | 8–10 |
| 2 | Thu Oct 15 | Email/WeChat a second wave; post to a different class; check progress | +10 (cumul. 18–20) |
| 3 | Fri Oct 16 | Prolific top-up if < 20; otherwise 2nd wave to class | +8 (cumul. 26–28) |
| 4 | Sat Oct 17 | Prolific top-up to reach 30; final cleanup | +2–4 (cumul. 30) |
| — | Sun Oct 18 | Data analysis, write-up, README updates | — |
| — | Mon Oct 19 | **Phase 1 deadline** | — |

---

## 6. Compensation

- **Personal network:** ¥10 / participant (small red packet, WeChat Pay, or coffee voucher). Total ~¥100–150.
- **Prolific:** $1.5 / participant, paid by Prolific's built-in reward system. Total ~$30–45.
- **Free / volunteer:** acceptable for first 5 (close friends), explicitly note "no payment" in the survey A3 (consent).

Budget ceiling: **~¥200 / $30**. Anything over → switch to a smaller class.

---

## 7. Data management & privacy

- **No real names** collected. Participant ID is a random 6-character string I assign.
- Survey responses **with participant ID only** are stored in `data/cleaned/`.
- **No third-party data** scraped. All catalog data comes from TMDB.
- Survey platform responses (Google Forms export) live in `data/raw/` and are **not** committed to GitHub if they contain any direct identifiers; only the **hashed/ID-only** version is committed.
- Per PDF §3.1, I'll record the **collection period** in the Phase 1 report (Oct 14–17, 2026).

---

## 8. Risk register

| Risk | Mitigation |
|---|---|
| Don't reach 30 in 4 days | Open Prolific on Day 1 with a $3 reward to seed; expand posting to 3+ class groups |
| Many incomplete responses | Strict screening at A1/A2; partial responses (incomplete pre OR post) excluded from analysis per analysis plan |
| Order effect dominates | Pre-registered as a robustness check; if it does, we report the analysis with order as covariate and the bias interpretation |
| Quota imbalance on age | Don't enforce; just record; subgroup analysis in robustness checks |
| TMDB API rate-limit during testing | Implement client-side rate-limit (max 4 req/sec), and cache titles in the prototype so we don't re-fetch for every participant |

---

## 9. Checklist before opening recruitment

- [ ] Survey form built and tested end-to-end (1 test participant = me)
- [ ] Prototype URLs stable (deployed to GitHub Pages)
- [ ] Recruitment post reviewed for required language (screening + compensation)
- [ ] Compensation method ready (red packet loaded, Prolific account funded)
- [ ] Daily check-in time set (e.g. every evening 9pm: count responses, decide next day's push)
- [ ] Amendments log in `docs/analysis-plan.md` ready to record any deviation
