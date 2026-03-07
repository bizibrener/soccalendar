API_KEY = "26fd7fd1d918475c96092189f2d88d99"
BASE_URL = "https://api.football-data.org/v4"

TEAMS = {
    # La Liga
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
    "atletico-madrid": {
        "id": 78,
        "name": "Atlético Madrid",
        "slug": "atletico-madrid",
        "crest": "https://crests.football-data.org/78.png",
        "league": "la-liga",
    },
    # Premier League
    "manchester-city": {
        "id": 65,
        "name": "Manchester City FC",
        "slug": "manchester-city",
        "crest": "https://crests.football-data.org/65.png",
        "league": "premier-league",
    },
    "manchester-united": {
        "id": 66,
        "name": "Manchester United FC",
        "slug": "manchester-united",
        "crest": "https://crests.football-data.org/66.png",
        "league": "premier-league",
    },
    "arsenal": {
        "id": 57,
        "name": "Arsenal FC",
        "slug": "arsenal",
        "crest": "https://crests.football-data.org/57.png",
        "league": "premier-league",
    },
    "liverpool": {
        "id": 64,
        "name": "Liverpool FC",
        "slug": "liverpool",
        "crest": "https://crests.football-data.org/64.png",
        "league": "premier-league",
    },
    "tottenham": {
        "id": 73,
        "name": "Tottenham Hotspur FC",
        "slug": "tottenham",
        "crest": "https://crests.football-data.org/73.png",
        "league": "premier-league",
    },
    "chelsea": {
        "id": 61,
        "name": "Chelsea FC",
        "slug": "chelsea",
        "crest": "https://crests.football-data.org/61.png",
        "league": "premier-league",
    },
    # Bundesliga
    "bayern-munich": {
        "id": 5,
        "name": "FC Bayern München",
        "slug": "bayern-munich",
        "crest": "https://crests.football-data.org/5.png",
        "league": "bundesliga",
    },
    "borussia-dortmund": {
        "id": 4,
        "name": "Borussia Dortmund",
        "slug": "borussia-dortmund",
        "crest": "https://crests.football-data.org/4.png",
        "league": "bundesliga",
    },
    # Serie A
    "juventus": {
        "id": 109,
        "name": "Juventus FC",
        "slug": "juventus",
        "crest": "https://crests.football-data.org/109.png",
        "league": "serie-a",
    },
    "ac-milan": {
        "id": 98,
        "name": "AC Milan",
        "slug": "ac-milan",
        "crest": "https://crests.football-data.org/98.png",
        "league": "serie-a",
    },
    "inter-milan": {
        "id": 108,
        "name": "FC Internazionale Milano",
        "slug": "inter-milan",
        "crest": "https://crests.football-data.org/108.png",
        "league": "serie-a",
    },
    "napoli": {
        "id": 113,
        "name": "SSC Napoli",
        "slug": "napoli",
        "crest": "https://crests.football-data.org/113.png",
        "league": "serie-a",
    },
    "roma": {
        "id": 100,
        "name": "AS Roma",
        "slug": "roma",
        "crest": "https://crests.football-data.org/100.png",
        "league": "serie-a",
    },
    # Ligat Ha'al
    "maccabi-tel-aviv": {
        "id": 134315,
        "name": "מכבי תל אביב",
        "slug": "maccabi-tel-aviv",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/lh08ob1625167121.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "hapoel-beer-sheva": {
        "id": 134799,
        "name": "הפועל באר שבע",
        "slug": "hapoel-beer-sheva",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/978vgx1579019997.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "beitar-jerusalem": {
        "id": 135992,
        "name": "בית״ר ירושלים",
        "slug": "beitar-jerusalem",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/bq7vys1639433460.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "hapoel-tel-aviv": {
        "id": 134124,
        "name": "הפועל תל אביב",
        "slug": "hapoel-tel-aviv",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/viqboc1579020034.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "maccabi-haifa": {
        "id": 134400,
        "name": "מכבי חיפה",
        "slug": "maccabi-haifa",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/t73b501639433206.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "hapoel-jerusalem": {
        "id": 141235,
        "name": "הפועל ירושלים",
        "slug": "hapoel-jerusalem",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/cvh4ec1639431062.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "maccabi-netanya": {
        "id": 134087,
        "name": "מכבי נתניה",
        "slug": "maccabi-netanya",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/xqrw8z1639430750.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "bnei-sakhnin": {
        "id": 135994,
        "name": "בני סכנין",
        "slug": "bnei-sakhnin",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/kbgr2l1639433190.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    "hapoel-haifa": {
        "id": 135995,
        "name": "הפועל חיפה",
        "slug": "hapoel-haifa",
        "crest": "https://r2.thesportsdb.com/images/media/team/badge/ytmoe71639433126.png",
        "league": "ligat-haal",
        "provider": "thesportsdb_team",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
    },
    # Ligue 1
    "psg": {
        "id": 524,
        "name": "Paris Saint-Germain FC",
        "slug": "psg",
        "crest": "https://crests.football-data.org/524.png",
        "league": "ligue-1",
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
    "big-games": {
        "name": "Big Games",
        "slug": "big-games",
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
    "ligat-haal": {
        "name": "ליגת העל",
        "slug": "ligat-haal",
        "crest": "https://r2.thesportsdb.com/images/media/league/badge/glvhg51664190048.png",
        "provider": "thesportsdb_league",
        "thesportsdb_league_id": "4644",
        "thesportsdb_season": "2025-2026",
        "subtitle": "כל משחקי ליגת העל",
        "country": "israel",
        "flag_colors": ["#0038b8", "#fff", "#0038b8"],
    },
}

MATCH_DURATION_HOURS = 2
CALENDAR_DAYS_AHEAD = 14
CALENDAR_DAYS_BEHIND = 2

# API-Football (api-sports.io) — used for post-match stats
API_FOOTBALL_KEY = "9e37aa73a033f54b5dfebafc0b8b56fc"
API_FOOTBALL_BASE = "https://v3.football.api-sports.io"

# Map football-data.org competition codes to API-Football league IDs
COMPETITION_TO_APIFOOTBALL = {
    "PL": 39,       # Premier League
    "PD": 140,      # La Liga
    "BL1": 78,      # Bundesliga
    "SA": 135,       # Serie A
    "FL1": 61,       # Ligue 1
    "CL": 2,         # Champions League
    "Primera Division": 140,
    "Premier League": 39,
    "Bundesliga": 78,
    "Serie A": 135,
    "Ligue 1": 61,
    "UEFA Champions League": 2,
}
