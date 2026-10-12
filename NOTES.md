# AGENT NOTES — Soccalendar (read me first, saves tokens)

Owner: Bezalel. Personal project. Last updated: 2026-10-12 (refactor).

## What it is
A **personal** subscribable soccer calendar. Daily GitHub Action fetches matches, keeps the
"good" ones by a team-rating rule, writes `docs/calendar.ics`, hosted by GitHub Pages.
Subscribe once. No UI, no users, no server.
See `PLAN.md` for the decision history.

## Architecture (current branch `personal-refactor`)
- `rankings.py` — `TEAM_WEIGHTS` keyed by **football-data team ID** + `THRESHOLD`, `DAYS_AHEAD/BEHIND`. **The only file to edit to change content.**
- `providers/football_data.py` — chunked fetch of `/v4/matches` (free tier caps a query at 10 days). Reads key from env `FOOTBALL_DATA_KEY`.
- `build.py` — filter by rating → de-dupe by match id → write `docs/calendar.ics` (stable `UID=match-<id>@soccalendar`).
- `.github/workflows/build.yml` — daily cron 06:00 UTC, commits the `.ics`.
- `docs/calendar.ics` (generated) + `docs/index.html` (subscribe button, Pages from `/docs`).

## Selection rule
`weight(home) + weight(away) >= 4`. Ported from `soccer-to-calender-personal/Code/teams_list.py`,
but **keyed by team ID instead of name** — the old name-keyed version silently dropped Atlético
("Atlético de Madrid" ≠ API's "Club Atlético de Madrid"). PSG added at weight 3.

## Run locally
```bash
cd ~/myRepos/soccalendar
FOOTBALL_DATA_KEY=<key> ./venv/bin/python build.py   # writes docs/calendar.ics
```
Rebuild venv if broken: `rm -rf venv && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`

## GitHub / accounts (IMPORTANT)
- Remote: `https://github.com/bizibrener/soccalendar.git` (**personal account**, being made public).
- Machine has TWO `gh` accounts. Active/global = `bezalelbrener` (work) which **cannot** see this repo.
- This repo is set up **repo-locally** to use the personal token, so the global account is never touched:
  `credential.helper` (local) emits `bizibrener` + `gh auth token --user bizibrener`; `user.email=bizibrener@gmail.com`.
- Plain `git fetch/push` works here. **Do NOT `gh auth switch`.** For `gh` calls:
  `GH_TOKEN="$(gh auth token --user bizibrener)" gh ...`

## Secrets
- football-data key must live in GitHub Actions secret `FOOTBALL_DATA_KEY`, not in code.
- The old key `26fd7fd1...` is leaked in git history and in `soccer-to-calender-personal` — **rotate it**.

## Sister repo (archive)
- `~/myRepos/soccer-to-calender-personal` — old AWS Lambda + Terraform prototype that pushed events
  directly into Google Calendar. Source of the rating logic. Committed `service-credentials.json`
  and `token.pickle` — sensitive, don't reuse.
