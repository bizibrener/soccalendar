from flask import Flask, Response
from providers.barcelona import fetch_barcelona_matches
from ics_generator import generate_ics
from config import TEAMS

app = Flask(__name__)


@app.route("/")
def index():
    team_links = "".join(
        f'<li><a href="/calendar/{slug}">{info["name"]}</a></li>'
        for slug, info in TEAMS.items()
    )
    return f"""
    <html>
    <head><title>Soccalendar</title></head>
    <body>
        <h1>Soccalendar</h1>
        <p>Subscribe to soccer team calendars:</p>
        <ul>{team_links}</ul>
    </body>
    </html>
    """


PROVIDERS = {
    "barcelona": fetch_barcelona_matches,
}


@app.route("/calendar/<team_slug>")
def team_calendar(team_slug):
    if team_slug not in PROVIDERS:
        return "Team not found", 404

    team = TEAMS[team_slug]
    matches = PROVIDERS[team_slug]()
    ics_content = generate_ics(matches, team["name"])

    return Response(ics_content, mimetype="text/calendar")


if __name__ == "__main__":
    app.run(debug=True, port=5555)
