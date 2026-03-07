import datetime
import hashlib
from typing import List, Dict
from icalendar import Calendar, Event
from config import MATCH_DURATION_HOURS


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

        summary = f"{match['home_team']} vs {match['away_team']}"
        if match.get("competition"):
            summary += f" ({match['competition']})"

        event.add("summary", summary)
        event.add("dtstart", match["start_time"])
        event.add("dtend", match["start_time"] + datetime.timedelta(hours=MATCH_DURATION_HOURS))

        uid_source = f"{match['home_team']}-{match['away_team']}-{match['start_time'].isoformat()}"
        uid = hashlib.md5(uid_source.encode()).hexdigest() + "@soccalendar"
        event.add("uid", uid)

        event.add("dtstamp", datetime.datetime.now(datetime.timezone.utc))

        cal.add_component(event)

    return cal.to_ical().decode("utf-8")
