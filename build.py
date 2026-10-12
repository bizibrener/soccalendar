"""Build docs/calendar.ics — the subscribable feed.

Run:  FOOTBALL_DATA_KEY=xxx python build.py
CI:   GitHub Actions runs this daily and commits the updated file.
"""

import datetime
import os

from icalendar import Calendar, Event

from rankings import (
    TEAM_WEIGHTS, THRESHOLD, DAYS_AHEAD, DAYS_BEHIND,
    EXCLUDED_COMPETITIONS, COMPETITION_BONUS,
)
from providers.football_data import fetch_matches

OUT_PATH = os.path.join(os.path.dirname(__file__), "docs", "calendar.ics")
CALENDAR_NAME = "Good Soccer Games"
MATCH_HOURS = 2


def _weight(team_id) -> int:
    return TEAM_WEIGHTS.get(team_id, 0)


def _is_good(m) -> bool:
    if m["competition"] in EXCLUDED_COMPETITIONS:
        return False
    home, away = _weight(m["home_id"]), _weight(m["away_id"])
    threshold = THRESHOLD
    if m["competition"] in COMPETITION_BONUS and home > 0 and away > 0:
        threshold -= COMPETITION_BONUS[m["competition"]]
    return home + away >= threshold


def _summary(m) -> str:
    home, away = m["home_team"], m["away_team"]
    if m["status"] == "FINISHED" and m["score_home"] is not None:
        s = f"{home} {m['score_home']} - {m['score_away']} {away}"
    else:
        s = f"{home} vs {away}"
    if m.get("competition"):
        s += f" ({m['competition']})"
    return s


def build() -> int:
    matches = fetch_matches(DAYS_AHEAD, DAYS_BEHIND)
    good = [m for m in matches if _is_good(m)]

    # de-dupe by football-data match id (stable, so re-runs update instead of duplicating)
    seen, unique = set(), []
    for m in good:
        if m["id"] in seen:
            continue
        seen.add(m["id"])
        unique.append(m)
    unique.sort(key=lambda m: m["start_time"])

    cal = Calendar()
    cal.add("prodid", "-//Soccalendar//Personal//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", CALENDAR_NAME)
    cal.add("method", "PUBLISH")
    cal.add("refresh-interval;value=duration", "PT12H")
    cal.add("x-published-ttl", "PT12H")

    for m in unique:
        ev = Event()
        ev.add("summary", _summary(m))
        ev.add("dtstart", m["start_time"])
        ev.add("dtend", m["start_time"] + datetime.timedelta(hours=MATCH_HOURS))
        ev.add("uid", f"match-{m['id']}@soccalendar")
        ev.add("dtstamp", datetime.datetime.now(datetime.timezone.utc))
        if m.get("competition"):
            ev.add("description", m["competition"])
        cal.add_component(ev)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "wb") as f:
        f.write(cal.to_ical())
    return len(unique)


if __name__ == "__main__":
    n = build()
    print(f"Wrote {n} matches to {OUT_PATH}")
