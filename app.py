from flask import Flask, Response, render_template, request
from providers.fetch_matches import fetch_team_matches
from providers.fetch_important import fetch_important_matches
from providers.fetch_competition import fetch_competition_matches
from ics_generator import generate_ics
from config import TEAMS

app = Flask(__name__)


def get_matches(team_slug):
    team = TEAMS[team_slug]
    provider = team.get("provider", "team")

    if provider == "important":
        return fetch_important_matches()
    elif provider == "competition":
        return fetch_competition_matches(team["competition_code"])
    else:
        return fetch_team_matches(team_slug)


@app.route("/")
def index():
    return render_template("index.html", teams=TEAMS)


@app.route("/team/<team_slug>")
def team_page(team_slug):
    if team_slug not in TEAMS:
        return "Team not found", 404

    team = TEAMS[team_slug]
    base_url = request.host_url.rstrip("/")
    ics_path = f"/calendar/{team_slug}"
    https_url = f"{base_url}{ics_path}"
    webcal_url = https_url.replace("https://", "webcal://").replace("http://", "webcal://")

    return render_template("team.html", team=team, webcal_url=webcal_url, https_url=https_url)


@app.route("/calendar/<team_slug>")
def team_calendar(team_slug):
    if team_slug not in TEAMS:
        return "Team not found", 404

    team = TEAMS[team_slug]
    matches = get_matches(team_slug)
    ics_content = generate_ics(matches, team["name"])

    return Response(ics_content, mimetype="text/calendar")


if __name__ == "__main__":
    app.run(debug=True, port=5555)
