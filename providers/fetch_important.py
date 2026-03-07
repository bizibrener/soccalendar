import requests
import datetime
from typing import List, Dict
from config import API_KEY, BASE_URL, CALENDAR_DAYS_AHEAD, CALENDAR_DAYS_BEHIND

TEAM_RANKINGS = {
    "FC Barcelona": 4,
    "Real Madrid CF": 4,
    "Atlético de Madrid": 2,
    "Arsenal FC": 3,
    "Manchester City FC": 3,
    "Liverpool FC": 3,
    "FC Bayern München": 3,
    "Chelsea FC": 2,
    "Borussia Dortmund": 2,
    "Tottenham Hotspur FC": 2,
    "Manchester United FC": 1,
    "AC Milan": 2,
    "Juventus FC": 2,
}

RANK_THRESHOLD = 4


MAX_API_RANGE_DAYS = 10


def _fetch_matches_for_range(date_from, date_to) -> List[Dict]:
    url = f"{BASE_URL}/matches"
    headers = {"X-Auth-Token": API_KEY}
    params = {
        "dateFrom": date_from.strftime("%Y-%m-%d"),
        "dateTo": date_to.strftime("%Y-%m-%d"),
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("matches", [])
    except requests.RequestException as e:
        print(f"Error fetching matches: {e}")
        return []


def fetch_important_matches() -> List[Dict]:
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=CALENDAR_DAYS_BEHIND)
    end_date = today + datetime.timedelta(days=CALENDAR_DAYS_AHEAD)

    all_raw = []
    cursor = start_date
    while cursor < end_date:
        chunk_end = min(cursor + datetime.timedelta(days=MAX_API_RANGE_DAYS), end_date)
        all_raw.extend(_fetch_matches_for_range(cursor, chunk_end))
        cursor = chunk_end + datetime.timedelta(days=1)

    matches = []
    for match in all_raw:
        home = match.get("homeTeam", {}).get("name", "Unknown")
        away = match.get("awayTeam", {}).get("name", "Unknown")
        utc_date = match.get("utcDate", "")
        competition = match.get("competition", {}).get("name", "")

        if not utc_date:
            continue

        home_rank = TEAM_RANKINGS.get(home, 0)
        away_rank = TEAM_RANKINGS.get(away, 0)

        if home_rank == 0 and away_rank == 0:
            continue
        if home_rank + away_rank < RANK_THRESHOLD:
            continue

        start_time = datetime.datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

        status = match.get("status", "")
        score = match.get("score", {})

        match_data = {
            "home_team": home,
            "away_team": away,
            "start_time": start_time,
            "competition": competition,
            "status": status,
        }

        if status == "FINISHED":
            ft = score.get("fullTime", {})
            match_data["score_home"] = ft.get("home")
            match_data["score_away"] = ft.get("away")

        matches.append(match_data)

    return matches
