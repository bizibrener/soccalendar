import requests
import datetime
from typing import List, Dict
from config import API_KEY, BASE_URL, CALENDAR_DAYS_AHEAD


def fetch_competition_matches(competition_code: str) -> List[Dict]:
    url = f"{BASE_URL}/competitions/{competition_code}/matches"

    today = datetime.date.today()
    date_to = today + datetime.timedelta(days=CALENDAR_DAYS_AHEAD)

    headers = {"X-Auth-Token": API_KEY}
    params = {
        "dateFrom": today.strftime("%Y-%m-%d"),
        "dateTo": date_to.strftime("%Y-%m-%d"),
        "status": "SCHEDULED,TIMED",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching {competition_code} matches: {e}")
        return []

    matches = []
    for match in data.get("matches", []):
        home = match.get("homeTeam", {}).get("name", "Unknown")
        away = match.get("awayTeam", {}).get("name", "Unknown")
        utc_date = match.get("utcDate", "")

        if not utc_date:
            continue

        start_time = datetime.datetime.fromisoformat(
            utc_date.replace("Z", "+00:00")
        )

        matches.append({
            "home_team": home,
            "away_team": away,
            "start_time": start_time,
            "competition": competition_code,
        })

    return matches
