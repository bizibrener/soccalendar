# soccalander



## 📁 Suggested File Structure

```
soccer_calendar_platform/
│
├── calendars/                  # ICS files or dynamic routes for calendars
├── config/
│   └── settings.py             # API keys, refresh intervals, etc.
├── core/
│   ├── __init__.py
│   ├── base_calendar.py        # Abstract base calendar
│   ├── event.py                # Event model and parser
│   └── utils.py                # Time conversion, formatting, etc.
│
├── providers/                 # Specific league/team implementations
│   ├── barcelona.py
│   ├── real_madrid.py
│   ├── premier_league.py
│   └── champions_league.py
│
├── ics_generator/
│   └── generator.py            # Converts event objects to .ics files
│
├── scheduler/
│   └── updater.py              # Main script to pull + generate updates
│
├── web/
│   ├── app.py                  # Flask/FastAPI to serve .ics files
│   └── routes.py
│
├── requirements.txt
└── README.md
```
