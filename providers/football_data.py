"""Fetch matches from football-data.org (free tier)."""

import datetime
import os
import requests

BASE_URL = "https://api.football-data.org/v4"
MAX_RANGE_DAYS = 10  # free tier caps a single /matches query at 10 days


def _api_key() -> str:
    key = os.environ.get("FOOTBALL_DATA_KEY")
    if not key:
        raise RuntimeError(
            "FOOTBALL_DATA_KEY is not set. Locally: `export FOOTBALL_DATA_KEY=...`; "
            "in CI: add it as a GitHub Actions secret."
        )
    return key


def _fetch_range(date_from: datetime.date, date_to: datetime.date) -> list:
    resp = requests.get(
        f"{BASE_URL}/matches",
        headers={"X-Auth-Token": _api_key()},
        params={"dateFrom": date_from.isoformat(), "dateTo": date_to.isoformat()},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("matches", [])


def fetch_matches(days_ahead: int, days_behind: int = 0) -> list:
    """All matches in [today-days_behind, today+days_ahead], as plain dicts."""
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days_behind)
    end = today + datetime.timedelta(days=days_ahead)

    raw = []
    cursor = start
    while cursor < end:
        chunk_end = min(cursor + datetime.timedelta(days=MAX_RANGE_DAYS), end)
        raw.extend(_fetch_range(cursor, chunk_end))
        cursor = chunk_end + datetime.timedelta(days=1)

    matches = []
    for m in raw:
        utc = m.get("utcDate", "")
        if not utc:
            continue
        status = m.get("status", "")
        ft = m.get("score", {}).get("fullTime", {})
        matches.append({
            "id": m.get("id"),
            "home_team": m.get("homeTeam", {}).get("name", "Unknown"),
            "away_team": m.get("awayTeam", {}).get("name", "Unknown"),
            "home_id": m.get("homeTeam", {}).get("id"),
            "away_id": m.get("awayTeam", {}).get("id"),
            "start_time": datetime.datetime.fromisoformat(utc.replace("Z", "+00:00")),
            "competition": m.get("competition", {}).get("name", ""),
            "status": status,
            "score_home": ft.get("home") if status == "FINISHED" else None,
            "score_away": ft.get("away") if status == "FINISHED" else None,
        })
    return matches
