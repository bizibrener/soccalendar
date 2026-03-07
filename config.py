API_KEY = "26fd7fd1d918475c96092189f2d88d99"
BASE_URL = "https://api.football-data.org/v4"

TEAMS = {
    "barcelona": {
        "id": 81,
        "name": "FC Barcelona",
        "slug": "barcelona",
        "crest": "https://crests.football-data.org/81.png",
        "league": "la-liga",
    },
    "real-madrid": {
        "id": 86,
        "name": "Real Madrid CF",
        "slug": "real-madrid",
        "crest": "https://crests.football-data.org/86.png",
        "league": "la-liga",
    },
    "liverpool": {
        "id": 64,
        "name": "Liverpool FC",
        "slug": "liverpool",
        "crest": "https://crests.football-data.org/64.png",
        "league": "premier-league",
    },
    "manchester-united": {
        "id": 66,
        "name": "Manchester United FC",
        "slug": "manchester-united",
        "crest": "https://crests.football-data.org/66.png",
        "league": "premier-league",
    },
    "manchester-city": {
        "id": 65,
        "name": "Manchester City FC",
        "slug": "manchester-city",
        "crest": "https://crests.football-data.org/65.png",
        "league": "premier-league",
    },
    "arsenal": {
        "id": 57,
        "name": "Arsenal FC",
        "slug": "arsenal",
        "crest": "https://crests.football-data.org/57.png",
        "league": "premier-league",
    },
}

FEATURED = {
    "champions-league": {
        "name": "Champions League",
        "slug": "champions-league",
        "crest": "https://crests.football-data.org/CL.png",
        "provider": "competition",
        "competition_code": "CL",
        "subtitle": "For Champions League lovers",
    },
    "important-games": {
        "name": "Important Games",
        "slug": "important-games",
        "crest": "https://img.icons8.com/color/512/trophy.png",
        "provider": "important",
        "subtitle": "For those who just love soccer",
    },
}

LEAGUES = {
    "la-liga": {
        "name": "La Liga",
        "slug": "la-liga",
        "crest": "https://crests.football-data.org/PD.png",
        "provider": "competition",
        "competition_code": "PD",
        "subtitle": "All Spanish league matches",
        "country": "spain",
        "flag_colors": ["#c60b1e", "#ffc400", "#c60b1e"],
    },
    "premier-league": {
        "name": "Premier League",
        "slug": "premier-league",
        "crest": "https://crests.football-data.org/PL.png",
        "provider": "competition",
        "competition_code": "PL",
        "subtitle": "All English league matches",
        "country": "england",
        "flag_colors": ["#cf081f", "#fff", "#002366"],
    },
    "bundesliga": {
        "name": "Bundesliga",
        "slug": "bundesliga",
        "crest": "https://crests.football-data.org/BL1.png",
        "provider": "competition",
        "competition_code": "BL1",
        "subtitle": "All German league matches",
        "country": "germany",
        "flag_colors": ["#000", "#dd0000", "#ffcc00"],
    },
    "ligue-1": {
        "name": "Ligue 1",
        "slug": "ligue-1",
        "crest": "https://crests.football-data.org/FL1.png",
        "provider": "competition",
        "competition_code": "FL1",
        "subtitle": "All French league matches",
        "country": "france",
        "flag_colors": ["#002395", "#fff", "#ed2939"],
    },
    "serie-a": {
        "name": "Serie A",
        "slug": "serie-a",
        "crest": "https://crests.football-data.org/SA.png",
        "provider": "competition",
        "competition_code": "SA",
        "subtitle": "All Italian league matches",
        "country": "italy",
        "flag_colors": ["#009246", "#fff", "#ce2b37"],
    },
}

MATCH_DURATION_HOURS = 2
CALENDAR_DAYS_AHEAD = 14
