import requests
import json
import os
import datetime
from typing import Dict, Optional
from config import API_FOOTBALL_KEY, API_FOOTBALL_BASE, COMPETITION_TO_APIFOOTBALL

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".stats_cache")


def _get_cache_path(home: str, away: str, date_str: str) -> str:
    safe = f"{home}__{away}__{date_str}".replace(" ", "_").replace("/", "_")
    return os.path.join(CACHE_DIR, f"{safe}.json")


def _load_cached(path: str) -> Optional[Dict]:
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return None


def _save_cache(path: str, data: Dict):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f)


def _normalize_name(name: str) -> str:
    replacements = {
        "FC Barcelona": "Barcelona",
        "Real Madrid CF": "Real Madrid",
        "Club Atlético de Madrid": "Atletico Madrid",
        "Atlético Madrid": "Atletico Madrid",
        "Manchester City FC": "Manchester City",
        "Manchester United FC": "Manchester United",
        "Arsenal FC": "Arsenal",
        "Liverpool FC": "Liverpool",
        "Tottenham Hotspur FC": "Tottenham",
        "Chelsea FC": "Chelsea",
        "FC Bayern München": "Bayern Munich",
        "Borussia Dortmund": "Dortmund",
        "Juventus FC": "Juventus",
        "AC Milan": "AC Milan",
        "FC Internazionale Milano": "Inter",
        "SSC Napoli": "Napoli",
        "AS Roma": "Roma",
        "Paris Saint-Germain FC": "Paris Saint Germain",
    }
    return replacements.get(name, name)


def _teams_match(api_name: str, our_name: str) -> bool:
    a = _normalize_name(our_name).lower()
    b = api_name.lower()
    if a == b or a in b or b in a:
        return True
    a_words = set(a.split()) - {"fc", "cf", "sc", "rb", "ac", "as", "ss", "ssc", "vfl", "1."}
    b_words = set(b.split()) - {"fc", "cf", "sc", "rb", "ac", "as", "ss", "ssc", "vfl", "1."}
    return bool(a_words & b_words)


def fetch_match_stats(home: str, away: str, match_date: datetime.datetime,
                      competition: str = "") -> Optional[Dict]:
    if not API_FOOTBALL_KEY:
        return None

    date_str = match_date.strftime("%Y-%m-%d")

    cache_path = _get_cache_path(home, away, date_str)
    cached = _load_cached(cache_path)
    if cached is not None:
        return cached if cached.get("found") else None

    headers = {"x-apisports-key": API_FOOTBALL_KEY}

    # Free plan can't filter by league/season, so search all fixtures for the date
    try:
        resp = requests.get(f"{API_FOOTBALL_BASE}/fixtures", headers=headers,
                            params={"date": date_str, "status": "FT"},
                            timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        print(f"API-Football error: {e}")
        return None

    fixture = None
    for fx in data.get("response", []):
        fx_home = fx.get("teams", {}).get("home", {}).get("name", "")
        fx_away = fx.get("teams", {}).get("away", {}).get("name", "")
        if _teams_match(fx_home, home) and _teams_match(fx_away, away):
            fixture = fx
            break

    if not fixture:
        _save_cache(cache_path, {"found": False})
        return None

    fixture_id = fixture["fixture"]["id"]

    # Fetch events (goals, cards)
    events = []
    try:
        resp = requests.get(f"{API_FOOTBALL_BASE}/fixtures/events",
                            headers=headers, params={"fixture": fixture_id},
                            timeout=10)
        resp.raise_for_status()
        events = resp.json().get("response", [])
    except requests.RequestException:
        pass

    # Fetch statistics (possession, shots, etc.)
    stats_raw = []
    try:
        resp = requests.get(f"{API_FOOTBALL_BASE}/fixtures/statistics",
                            headers=headers, params={"fixture": fixture_id},
                            timeout=10)
        resp.raise_for_status()
        stats_raw = resp.json().get("response", [])
    except requests.RequestException:
        pass

    goals = []
    for ev in events:
        if ev.get("type") == "Goal" and ev.get("detail") != "Missed Penalty":
            goals.append({
                "minute": ev.get("time", {}).get("elapsed", "?"),
                "scorer": ev.get("player", {}).get("name", "Unknown"),
                "assist": ev.get("assist", {}).get("name"),
                "team": ev.get("team", {}).get("name", ""),
                "detail": ev.get("detail", ""),
            })

    stats = {}
    for team_stats in stats_raw:
        team_name = team_stats.get("team", {}).get("name", "")
        side = "home" if _teams_match(team_name, home) else "away"
        for s in team_stats.get("statistics", []):
            stat_type = s.get("type", "")
            stat_val = s.get("value")
            if stat_type not in stats:
                stats[stat_type] = {}
            stats[stat_type][side] = stat_val

    score = fixture.get("goals", {})

    result = {
        "found": True,
        "score_home": score.get("home"),
        "score_away": score.get("away"),
        "goals": goals,
        "stats": stats,
    }

    _save_cache(cache_path, result)
    return result


def format_stats_description(stats_data: Dict, home: str, away: str) -> str:
    if not stats_data or not stats_data.get("found"):
        return ""

    lines = []

    score_h = stats_data.get("score_home", "?")
    score_a = stats_data.get("score_away", "?")
    lines.append(f"Final Score: {home} {score_h} - {score_a} {away}")
    lines.append("")

    goals = stats_data.get("goals", [])
    if goals:
        lines.append("Goals:")
        for g in goals:
            detail = f" ({g['detail']})" if g.get("detail") and g["detail"] != "Normal Goal" else ""
            assist = f" (assist: {g['assist']})" if g.get("assist") else ""
            lines.append(f"  {g['minute']}' {g['scorer']}{assist}{detail}")
        lines.append("")

    st = stats_data.get("stats", {})
    possession = st.get("Ball Possession", {})
    if possession.get("home") and possession.get("away"):
        lines.append(f"Possession: {home} {possession['home']} - {possession['away']} {away}")

    shots = st.get("Total Shots", {})
    shots_on = st.get("Shots on Goal", {})
    if shots.get("home") is not None:
        lines.append(f"Shots: {shots.get('home', 0)} - {shots.get('away', 0)}"
                      f"  (on target: {shots_on.get('home', 0)} - {shots_on.get('away', 0)})")

    corners = st.get("Corner Kicks", {})
    if corners.get("home") is not None:
        lines.append(f"Corners: {corners.get('home', 0)} - {corners.get('away', 0)}")

    xg = st.get("expected_goals", {})
    if xg.get("home") is not None:
        lines.append(f"xG: {xg.get('home', '-')} - {xg.get('away', '-')}")

    return "\n".join(lines)
