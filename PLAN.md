# PLAN — Soccalendar → personal "just put the good games in my calendar"

Decided 2026-10-12. Owner: Bezalel. Status: **proposed, not yet executed.**

## Goal
One subscribable `.ics` calendar containing every "good enough" soccer match, auto-refreshed
daily, zero servers to babysit. No UI, no sharing, no per-team pages. Just: pick a rating rule
→ file → subscribe once in Google Calendar.

## Decisions (locked)
- **Hosting:** zero-ops — GitHub Actions cron regenerates the file; GitHub Pages serves it.
- **Calendar app:** Google Calendar.
- **Selection rule:** *rating only* — a match is in the calendar iff `weight(home) + weight(away) >= 4`.
- **Rankings:** keep the existing 13 teams + weights, fix the bugs.

## Target architecture
```
rankings.py                         # team weights (keyed by football-data TEAM ID) + threshold + window
build.py                            # fetch all matches in window -> filter by rating -> dedupe -> docs/calendar.ics
providers/football_data.py          # chunked /v4/matches fetch (reuse the 10-day chunking already in fetch_important.py)
docs/calendar.ics                   # GENERATED artifact, committed by CI, served by GitHub Pages
docs/index.html                     # optional tiny page with an "Add to Google Calendar" button
.github/workflows/build.yml         # daily cron: install deps, run build.py, commit if changed
requirements.txt                    # requests, icalendar   (drop flask/gunicorn)
```
Subscribe URL: `https://bizibrener.github.io/soccalendar/calendar.ics`

## Selection rule (ported from `soccer-to-calender-personal/Code/teams_list.py`)
Weights (unchanged): Barcelona 4, Real Madrid 4 · Arsenal/Man City/Liverpool/Bayern 3 ·
Atlético/Chelsea/Dortmund/Tottenham/Milan/Juventus 2 · Man Utd 1.
Rule: `sum >= 4`; two unranked teams skipped.

### Bugs being fixed
1. **Name matching → ID matching.** Old code keyed on strings like `"Atlético de Madrid"`, but the API
   returns `"Club Atlético de Madrid"` → Atlético silently scored 0 and **every Atlético game was
   dropped**. New code keys on `team.id` (robust forever). Same fix also unbreaks "Big Games" in the old app.
2. **PSG missing** from the table (was scoring 0 by accident). Adding it — *weight TBD, see open items*.
3. **Secrets**: `API_KEY` is hardcoded in `config.py` today. Move to env var `FOOTBALL_DATA_KEY`,
   supplied by a GitHub Actions secret. (Also **rotate the current key** — it's leaked in git history,
   and again in the `soccer-to-calender-personal` repo.)

## Football-data team IDs (for the ID-based table)
Barcelona 81 · Real Madrid 86 · Atlético 78 · Man City 65 · Man Utd 66 · Arsenal 57 · Liverpool 64 ·
Tottenham 73 · Chelsea 61 · Bayern 5 · Dortmund 4 · Juventus 109 · AC Milan 98 · PSG 524.

## Build logic (`build.py`)
1. Window: `today` → `today + 14d` (chunk API calls to ≤10 days, free-tier limit).
2. Fetch `/v4/matches` for the whole window (free-tier competitions come back automatically).
3. Keep a match iff `weight[id(home)] + weight[id(away)] >= 4`.
4. Dedupe by `match.id`.
5. Emit `docs/calendar.ics`:
   - stable `UID = match-<match.id>@soccalendar` (so re-runs *update*, never duplicate),
   - `SUMMARY = "Home vs Away (Competition)"`, 2h duration, `refresh-interval PT12H`.
   - Optional: include finished games (last 2 days) with score in the summary.

## One-time manual setup (you + me)
1. Scrub secrets from code; add `FOOTBALL_DATA_KEY` as an Actions **secret**.
2. Enable **GitHub Pages** on the repo (branch `main`, folder `/docs`).
   - ⚠️ Pages on a **private** repo needs GitHub Pro; on Free it must be **public**. See open items.
3. Add the workflow; let it run once; grab the Pages URL.
4. Google Calendar → *Other calendars* → **From URL** → paste
   `https://bizibrener.github.io/soccalendar/calendar.ics`.

## What gets deleted
`app.py`, `templates/`, `Procfile`, `providers/fetch_important.py`, `providers/fetch_thesportsdb.py`
(Israeli — per your call), `providers/fetch_matches.py`, `providers/fetch_competition.py`,
`players/fetch_stats.py` (API-Football stats — not needed for a forward-looking feed), `config.py`.

## Known trade-off
Google Calendar subscribed feeds refresh ~12–24h and **don't fire reminders**. If you later want
kickoff notifications, we add a small reminder path (or you set one rule in Calendar). Not now.

## Open items before I build
- [x] **PSG weight** → **3**.
- [x] **Repo visibility** → **public** (rotate the leaked API key first).
- [x] **Window length** → **14 days**.

## Status — SHIPPED & LIVE (2026-10-12)
Merged to `main`. Repo is public. GitHub Pages enabled (`main` / `/docs`). Actions secret
`FOOTBALL_DATA_KEY` set. Daily workflow runs and commits `docs/calendar.ics`.

- **Feed:** https://bizibrener.github.io/soccalendar/calendar.ics (verified: `text/calendar`, 11 events)
- **Subscribe page:** https://bizibrener.github.io/soccalendar/
- **Google Calendar:** Other calendars → "+" → **From URL** → paste the feed URL.

### Selection rule (after the taste game)
`weight(home) + weight(away) >= 4`, minus `EXCLUDED_COMPETITIONS` (Serie A, Brasileirão,
Copa Libertadores), plus a UCL bonus of 1 that applies only when both teams are rated.
Fits 29/29 of the owner's gut calls. Barca + Real are weight 4 → always in (owner is a Barca fan).

### Left to do (optional, not blocking)
- Rotate the football-data.org key when convenient (it's in git history). Fastest: register a
  fresh account (no regenerate button exists) and update the secret:
  `gh secret set FOOTBALL_DATA_KEY --repo bizibrener/soccalendar`.
- Maybe reduce commit churn: `DTSTAMP` changes every run, so the bot commits daily even when
  fixtures are unchanged. Harmless; could be diffed away later.
