API_KEY = "26fd7fd1d918475c96092189f2d88d99"
BASE_URL = "https://api.football-data.org/v4"

TEAMS = {
    "barcelona": {
        "id": 81,
        "name": "FC Barcelona",
        "slug": "barcelona",
        "crest": "https://crests.football-data.org/81.png",
    },
    "real-madrid": {
        "id": 86,
        "name": "Real Madrid CF",
        "slug": "real-madrid",
        "crest": "https://crests.football-data.org/86.png",
    },
    "liverpool": {
        "id": 64,
        "name": "Liverpool FC",
        "slug": "liverpool",
        "crest": "https://crests.football-data.org/64.png",
    },
    "manchester-united": {
        "id": 66,
        "name": "Manchester United FC",
        "slug": "manchester-united",
        "crest": "https://crests.football-data.org/66.png",
    },
    "manchester-city": {
        "id": 65,
        "name": "Manchester City FC",
        "slug": "manchester-city",
        "crest": "https://crests.football-data.org/65.png",
    },
    "champions-league": {
        "name": "Champions League",
        "slug": "champions-league",
        "crest": "https://crests.football-data.org/CL.png",
        "provider": "competition",
        "competition_code": "CL",
    },
    "important-games": {
        "name": "Important Games",
        "slug": "important-games",
        "crest": "https://img.icons8.com/color/512/trophy.png",
        "provider": "important",
    },
}

MATCH_DURATION_HOURS = 2
CALENDAR_DAYS_AHEAD = 14
