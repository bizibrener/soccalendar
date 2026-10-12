"""Team importance weights — the ONLY file you edit to change what shows up.

Keyed by football-data.org team ID (NOT name), so a team can never be silently
dropped by a naming mismatch (that bug is why Atlético never appeared before).

A match is "good enough" when:  weight(home) + weight(away) >= THRESHOLD
"""

TEAM_WEIGHTS = {
    # 4 — always worth watching
    81: 4,    # FC Barcelona
    86: 4,    # Real Madrid CF
    # 3 — big clubs; qualify vs anyone ranked
    57: 3,    # Arsenal FC
    65: 3,    # Manchester City FC
    64: 3,    # Liverpool FC
    5: 3,     # FC Bayern München
    524: 3,   # Paris Saint-Germain FC
    # 2 — strong; need a 2+ opponent (or ride a 3/4)
    78: 2,    # Club Atlético de Madrid
    61: 2,    # Chelsea FC
    4: 2,     # Borussia Dortmund
    73: 2,    # Tottenham Hotspur FC
    98: 2,    # AC Milan
    109: 2,   # Juventus FC
    # 1 — only interesting against a 3+
    66: 1,    # Manchester United FC
}

THRESHOLD = 4      # sum of both teams' weights must be >= this
DAYS_AHEAD = 14    # how far into the future the calendar looks
DAYS_BEHIND = 0    # include recently finished games (0 = forward-looking only)
