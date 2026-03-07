import datetime
import hashlib
from typing import List, Dict
from icalendar import Calendar, Event
from config import MATCH_DURATION_HOURS
from providers.fetch_stats import fetch_match_stats, format_stats_description


def generate_ics(matches: List[Dict], team_name: str) -> str:
    cal = Calendar()
    cal.add("prodid", "-//Soccalendar//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", f"{team_name} Matches")
    cal.add("x-wr-timezone", "UTC")
    cal.add("method", "PUBLISH")
    cal.add("refresh-interval;value=duration", "PT12H")
    cal.add("x-published-ttl", "PT12H")

    for match in matches:
        event = Event()
        home = match["home_team"]
        away = match["away_team"]
        is_finished = match.get("status") == "FINISHED"

        summary = f"{home} vs {away}"
        if is_finished:
            sh = match.get("score_home", "?")
            sa = match.get("score_away", "?")
            summary = f"{home} {sh} - {sa} {away}"
        if match.get("competition"):
            summary += f" ({match['competition']})"

        event.add("summary", summary)
        event.add("dtstart", match["start_time"])
        event.add("dtend", match["start_time"] + datetime.timedelta(hours=MATCH_DURATION_HOURS))

        if is_finished:
            stats = fetch_match_stats(home, away, match["start_time"],
                                      match.get("competition", ""))
            description = format_stats_description(stats, home, away)
            if description:
                event.add("description", description)

        uid_source = f"{home}-{away}-{match['start_time'].isoformat()}"
        uid = hashlib.md5(uid_source.encode()).hexdigest() + "@soccalendar"
        event.add("uid", uid)

        event.add("dtstamp", datetime.datetime.now(datetime.timezone.utc))

        cal.add_component(event)

    return cal.to_ical().decode("utf-8")
