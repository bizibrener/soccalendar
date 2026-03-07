import requests
import datetime
import json
import os
import time
from typing import List, Dict
from config import CALENDAR_DAYS_AHEAD, CALENDAR_DAYS_BEHIND

THESPORTSDB_BASE = "https://www.thesportsdb.com/api/v1/json/123"
ROUNDS_TO_SCAN = 6

HEBREW_NAMES = {
    "Maccabi Tel Aviv": "מכבי תל אביב",
    "Hapoel Be'er Sheva": "הפועל באר שבע",
    "Beitar Jerusalem": "בית״ר ירושלים",
    "Hapoel Tel-Aviv": "הפועל תל אביב",
    "Maccabi Haifa": "מכבי חיפה",
    "Hapoel Jerusalem": "הפועל ירושלים",
    "Maccabi Netanya": "מכבי נתניה",
    "Bnei Sakhnin": "בני סכנין",
    "Hapoel Haifa": "הפועל חיפה",
    "Hapoel Ironi Kiryat Shmona": "הפועל עירוני קריית שמונה",
    "Hapoel Petah Tikva": "הפועל פתח תקווה",
    "Ironi Tiberias": "עירוני טבריה",
    "Maccabi Bnei Raina": "מכבי בני ריינה",
    "FC Ashdod": "מ.ס. אשדוד",
}
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".thesportsdb_cache")
CACHE_TTL_HOURS = 6
REQUEST_DELAY = 2.5


def fetch_thesportsdb_league(league_id: str, season: str) -> List[Dict]:
    """Fetch upcoming + recent matches for an entire league from TheSportsDB."""
    today = datetime.date.today()
    date_from = today - datetime.timedelta(days=CALENDAR_DAYS_BEHIND)
    date_to = today + datetime.timedelta(days=CALENDAR_DAYS_AHEAD)

    events = _fetch_rounds(league_id, season, date_from, date_to)
    return [_to_match(e) for e in events]


def fetch_thesportsdb_team(team_name: str, league_id: str, season: str) -> List[Dict]:
    """Fetch upcoming + recent matches for a specific team from TheSportsDB."""
    today = datetime.date.today()
    date_from = today - datetime.timedelta(days=CALENDAR_DAYS_BEHIND)
    date_to = today + datetime.timedelta(days=CALENDAR_DAYS_AHEAD)

    all_events = _fetch_rounds(league_id, season, date_from, date_to)

    team_lower = team_name.lower()
    team_events = [
        e for e in all_events
        if team_lower in e.get("strHomeTeam", "").lower()
        or team_lower in e.get("strAwayTeam", "").lower()
    ]

    return [_to_match(e) for e in team_events]


def _fetch_rounds(league_id, season, date_from, date_to):
    """Fetch events by scanning rounds around the current matchday."""
    current_round = _find_current_round(league_id, season)
    start_round = max(1, current_round - 2)
    end_round = current_round + ROUNDS_TO_SCAN

    events = []
    seen_ids = set()

    for r in range(start_round, end_round + 1):
        round_events = _fetch_round_cached(league_id, season, r)
        for e in round_events:
            event_date = e.get("dateEvent", "")
            eid = e.get("idEvent")
            if eid in seen_ids:
                continue
            if date_from.isoformat() <= event_date <= date_to.isoformat():
                events.append(e)
                seen_ids.add(eid)

    return events


def _api_get(url, params):
    """Rate-limited API request."""
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _fetch_round_cached(league_id, season, round_num):
    """Fetch a single round with file-based caching."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_key = f"{league_id}_{season}_{round_num}.json"
    cache_path = os.path.join(CACHE_DIR, cache_key)

    if os.path.exists(cache_path):
        age_hours = (datetime.datetime.now().timestamp() - os.path.getmtime(cache_path)) / 3600
        if age_hours < CACHE_TTL_HOURS:
            with open(cache_path) as f:
                return json.load(f)

    try:
        data = _api_get(f"{THESPORTSDB_BASE}/eventsround.php",
                        {"id": league_id, "r": round_num, "s": season})
        events = data.get("events") or []
        with open(cache_path, "w") as f:
            json.dump(events, f)
        return events
    except Exception as ex:
        print(f"TheSportsDB round {round_num} fetch error: {ex}")
        if os.path.exists(cache_path):
            with open(cache_path) as f:
                return json.load(f)
        return []


def _find_current_round(league_id, season):
    """Determine the current round, cached to avoid extra API calls."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{league_id}_current_round.json")

    if os.path.exists(cache_path):
        age_hours = (datetime.datetime.now().timestamp() - os.path.getmtime(cache_path)) / 3600
        if age_hours < CACHE_TTL_HOURS:
            with open(cache_path) as f:
                return json.load(f).get("round", 1)

    current = 1
    try:
        data = _api_get(f"{THESPORTSDB_BASE}/eventspastleague.php", {"id": league_id})
        events = data.get("events") or []
        if events:
            current = int(events[0].get("intRound", 1))
    except Exception:
        try:
            data = _api_get(f"{THESPORTSDB_BASE}/eventsnextleague.php", {"id": league_id})
            events = data.get("events") or []
            if events:
                current = int(events[0].get("intRound", 1))
        except Exception:
            pass

    with open(cache_path, "w") as f:
        json.dump({"round": current}, f)
    return current


def _to_match(event: Dict) -> Dict:
    """Convert a TheSportsDB event to our standard match dict."""
    home_en = event.get("strHomeTeam", "Unknown")
    away_en = event.get("strAwayTeam", "Unknown")
    home = HEBREW_NAMES.get(home_en, home_en)
    away = HEBREW_NAMES.get(away_en, away_en)
    timestamp = event.get("strTimestamp", "")
    date_str = event.get("dateEvent", "")
    time_str = event.get("strTime", "00:00:00")

    start_time = None
    if timestamp:
        try:
            dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            start_time = dt
        except ValueError:
            pass
    if start_time is None:
        start_time = _parse_date_time(date_str, time_str)

    home_score = event.get("intHomeScore")
    away_score = event.get("intAwayScore")
    is_finished = home_score is not None and away_score is not None

    status_str = event.get("strStatus", "")
    if status_str == "Match Postponed":
        api_status = "POSTPONED"
    elif is_finished:
        api_status = "FINISHED"
    else:
        api_status = "SCHEDULED"

    match_data = {
        "home_team": home,
        "away_team": away,
        "start_time": start_time,
        "competition": "ליגת העל",
        "status": api_status,
    }

    if is_finished:
        match_data["score_home"] = home_score
        match_data["score_away"] = away_score

    return match_data


def _parse_date_time(date_str, time_str):
    try:
        dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        return dt.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return dt.replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            return datetime.datetime.now(datetime.timezone.utc)
