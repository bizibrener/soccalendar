# Soccalendar

A single subscribable soccer calendar. A daily GitHub Action fetches upcoming matches,
keeps the "good" ones (by a team-rating rule), and writes `docs/calendar.ics`, which is
served statically by GitHub Pages. Subscribe once in Google/Apple Calendar and forget it.

## How it works

```
rankings.py                   # team weights + threshold — the only file you edit
providers/football_data.py    # fetches matches from football-data.org
build.py                      # filter by rating -> docs/calendar.ics
.github/workflows/build.yml   # runs daily, commits the updated .ics
docs/calendar.ics             # the generated feed (served by GitHub Pages)
```

### Selection rule
A match is included when `weight(home) + weight(away) >= THRESHOLD` (default 4).
Weights live in `rankings.py`, keyed by **football-data team ID** (not name — names caused
teams to silently disappear). Two unranked teams are never included.

## Run locally

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
FOOTBALL_DATA_KEY=<your key> python build.py
# -> writes docs/calendar.ics
```

Get a free API key at https://www.football-data.org/client/register.

## Deploy

- GitHub Actions runs `build.py` daily and commits `docs/calendar.ics`.
- The API key is stored as the Actions secret **`FOOTBALL_DATA_KEY`** (never in the repo).
- GitHub Pages serves the file from `main` / `/docs`.
- Subscribe at: `https://bizibrener.github.io/soccalendar/calendar.ics`
  (or open `docs/index.html` mentally — it has an "Add to Google Calendar" button.)

## Change what's in the calendar

Edit `TEAM_WEIGHTS` and/or `THRESHOLD` in `rankings.py`, commit, and the next run picks it up.
Same file also controls `DAYS_AHEAD` (how far forward it looks).

## Note
Google Calendar refreshes subscribed feeds every ~12–24h and does not fire reminders for them.
