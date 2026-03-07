from flask import Flask, Response, render_template, request
from providers.fetch_matches import fetch_team_matches
from providers.fetch_important import fetch_important_matches
from providers.fetch_competition import fetch_competition_matches
from providers.fetch_thesportsdb import fetch_thesportsdb_league, fetch_thesportsdb_team
from ics_generator import generate_ics
from config import TEAMS, FEATURED, LEAGUES

app = Flask(__name__)

ALL_CALENDARS = {**FEATURED, **LEAGUES, **TEAMS}


def get_matches(slug):
    cal = ALL_CALENDARS[slug]
    provider = cal.get("provider", "team")

    if provider == "important":
        return fetch_important_matches()
    elif provider == "competition":
        return fetch_competition_matches(cal["competition_code"])
    elif provider == "thesportsdb_league":
        return fetch_thesportsdb_league(cal["thesportsdb_league_id"], cal["thesportsdb_season"])
    elif provider == "thesportsdb_team":
        return fetch_thesportsdb_team(cal["name"], cal["thesportsdb_league_id"], cal["thesportsdb_season"])
    else:
        return fetch_team_matches(slug)


@app.route("/")
def index():
    return render_template("index.html", featured=FEATURED, leagues=LEAGUES, teams=TEAMS)


@app.route("/team/<team_slug>")
def team_page(team_slug):
    if team_slug not in ALL_CALENDARS:
        return "Team not found", 404

    team = ALL_CALENDARS[team_slug]
    base_url = request.host_url.rstrip("/")
    ics_path = f"/calendar/{team_slug}"
    https_url = f"{base_url}{ics_path}"
    webcal_url = https_url.replace("https://", "webcal://").replace("http://", "webcal://")

    return render_template("team.html", team=team, webcal_url=webcal_url, https_url=https_url)


@app.route("/calendar/<team_slug>")
def team_calendar(team_slug):
    if team_slug not in ALL_CALENDARS:
        return "Team not found", 404

    team = ALL_CALENDARS[team_slug]
    matches = get_matches(team_slug)
    ics_content = generate_ics(matches, team["name"])

    return Response(ics_content, mimetype="text/calendar")


if __name__ == "__main__":
    app.run(debug=True, port=5555)
