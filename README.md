# Soccalendar

Subscribable soccer match calendars. Users pick a team, click subscribe, and get auto-updating match events in their calendar app (Google Calendar, Apple Calendar, Outlook).

## Live URL

Hosted on **Railway**: https://soccalendar-production.up.railway.app

Railway auto-deploys on every push to `main`.

## Tech Stack

- **Backend**: Python / Flask
- **Calendar format**: `.ics` (iCalendar) via the `icalendar` library
- **Soccer data**: [football-data.org](https://www.football-data.org/) API (v4), free tier
- **WSGI server**: Gunicorn (production), Flask dev server (local)
- **Hosting**: Railway (free trial, then pay-as-you-go)

## Project Structure

```
soccalendar/
├── app.py                      # Flask app — routes for landing page, team pages, and .ics feeds
├── config.py                   # API key, team definitions (id, name, crest URL), settings
├── ics_generator.py            # Converts match list to .ics calendar string
├── providers/
│   └── fetch_matches.py        # Generic provider — fetches matches for any team from football-data.org
├── templates/
│   ├── index.html              # Landing page — team cards with club color gradients and crests
│   └── team.html               # Team subscribe page — buttons for Google/Apple/Outlook
├── Procfile                    # Railway/Heroku start command (gunicorn app:app)
├── requirements.txt            # Python dependencies
└── README.md
```

## How It Works

1. `GET /` — Landing page with team cards
2. `GET /team/<slug>` — Subscribe page with platform-specific buttons (Google Calendar, Apple Calendar, Outlook)
3. `GET /calendar/<slug>` — Raw `.ics` feed (this is the URL calendar apps subscribe to)

The `.ics` feed is generated dynamically on each request — it calls the football-data.org API for the team's upcoming matches (next 14 days) and returns a valid iCalendar file. Calendar apps re-fetch this URL periodically (~12-24h) to pick up new games.

## Adding a New Team

1. **Find the team ID** on football-data.org: `GET https://api.football-data.org/v4/teams?name=<search>` (with `X-Auth-Token` header)
2. **Add an entry to `TEAMS`** in `config.py`:
   ```python
   "team-slug": {
       "id": <football-data-team-id>,
       "name": "Display Name",
       "slug": "team-slug",
       "crest": "https://crests.football-data.org/<id>.png",
   },
   ```
3. **Add CSS colors** in `templates/index.html`:
   ```css
   .team-slug .bg {
       background: linear-gradient(135deg, #color1 0%, #color2 100%);
   }
   ```
4. Push to `main` — Railway auto-deploys.

## API Limitations

- **Free tier** of football-data.org includes: La Liga, Premier League, Champions League, Bundesliga, Serie A, Ligue 1, Eredivisie, Primeira Liga, Championship, Brasileirao, World Cup, Euros.
- **Not included** in free tier: Copa del Rey, FA Cup, domestic cups, Conference League, etc. Upgrading to a paid tier (starts at 49 EUR/month) would add these.
- API key is hardcoded in `config.py` (should be moved to env var for production).
- Rate limit: 10 requests/minute on the free tier.

## Running Locally

```bash
cd soccalendar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
# Open http://localhost:5555
```

## Known Limitations / Future Ideas

- Event colors cannot be set via `.ics` — subscribers choose their own color in their calendar app.
- Google Calendar refreshes subscribed calendars every ~12-24 hours (not configurable).
- No caching — each request to `/calendar/<slug>` hits the football-data.org API. Could add caching to reduce API calls if traffic grows.
- Landing page and team pages are server-rendered HTML. Could be upgraded to a proper frontend framework if needed.
- Domain `soccalendar.com` was considered but not yet configured. DNS would need CNAME pointed to Railway.
