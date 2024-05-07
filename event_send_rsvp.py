from exchangelib import Credentials, Account, Configuration, EWSDateTime, EWSTimeZone, CalendarItem
from exchangelib.items import SEND_ONLY
from datetime import datetime, timedelta
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

# Define the start and end times for the query
tz = EWSTimeZone("America/New_York")
now = datetime.now()
end_time = now + timedelta(days=30)
start = EWSDateTime(now.year, now.month, now.day, tzinfo=tz)
end = EWSDateTime(end_time.year, end_time.month, end_time.day, tzinfo=tz)

# Query for primary calendar events
calendar_items = account.calendar.view(start=start, end=end)
print("Primary calendar events:")
for item in calendar_items:
    if isinstance(item, CalendarItem):
        item = account.calendar.get(id=item.id)
        print("subject:", item.subject, "start:", item.start, "id:", item.id)

# Respond to an event
event_id = 'AAMkAGY0ODk4NjA1LTc5MWQtNDE0NS1iMmJkLTk5YzYxZjk2NzY5YQFRAAgI3HCEIrRAAEYAAAAAAP1kvVnViEqVb/Ymc6I43gcAqJTRI/07z06lEfGhzXbTqwAAAAABDQAAqJTRI/07z06lEfGhzXbTqwADJR1y3wAAEA=='
event = account.calendar.get(id=event_id)
returned = event.accept(message_disposition=SEND_ONLY)
print(f"{returned.__module__}.BulkCreateResult", returned)
# event.tentatively_accept(message_disposition=SEND_ONLY)
# event.decline(message_disposition=SEND_ONLY)
