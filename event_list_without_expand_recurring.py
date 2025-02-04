from exchangelib import Credentials, Account, Configuration, EWSDateTime, EWSTimeZone, CalendarItem
from datetime import datetime, timedelta
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('YODA_EMAIL_ADDRESS')
password = os.getenv('YODA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

start = datetime(2025, 2, 5, tzinfo=account.default_timezone)
end = datetime(2025, 2, 6, tzinfo=account.default_timezone)
events = account.calendar.view(start=start, end=end)

known_master_event_ids = set([])
for event in events:
    if event.recurrence_id is None:
        print(event.subject, event.start, event.end)
    else:
        master_event = event.recurring_master().refresh()
        if master_event.id not in known_master_event_ids:
            known_master_event_ids.add(master_event.id)
            print(master_event.subject, master_event.start, master_event.end)

