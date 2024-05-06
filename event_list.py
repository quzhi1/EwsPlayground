from exchangelib import Credentials, Account, Configuration, EWSDateTime, EWSTimeZone, CalendarItem
from datetime import datetime, timedelta
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

# Define the start and end times for the query
now = datetime.now()
end_time = now + timedelta(days=30)
start = EWSDateTime(now.year, now.month, now.day, tzinfo=EWSTimeZone.localzone())
end = EWSDateTime(end_time.year, end_time.month, end_time.day, tzinfo=EWSTimeZone.localzone())

# Query for primary calendar events
calendar_items = account.calendar.view(start=start, end=end)
print("Primary calendar events:")
for item in calendar_items:
    if isinstance(item, CalendarItem):
        item = account.calendar.get(id=item.id)
        print("subject:", item.subject, "start:", item.start, "id:", item.id)

# Find a secondary calendar
secondary_calendar = None
for folder in account.calendar.walk():
    if folder.folder_class == 'IPF.Appointment' and folder.name == "Writable Calendar":
        secondary_calendar = folder

# Query for secondary calendar events with filter
calendar_items = secondary_calendar.view(start=start, end=end)
print("Secondary calendar events:")
for item in calendar_items:
    if isinstance(item, CalendarItem):
        item = secondary_calendar.get(id=item.id)
        print("subject:", item.subject, "start:", item.start, "id:", item.id)

# Query for free-busy information
# attendee_type can be "Optional", "Organizer", "Required", "Resource", "Room"
accounts = [
    ("test@nylas.info", "Required", False),
    ("staging_test@nylas.info", "Required", False),
]
free_busy = account.protocol.get_free_busy_info(accounts=accounts, start=start, end=end, merged_free_busy_interval=30)
print("Free-busy information:")
for busy_info in free_busy:
    print("working_hours:", busy_info.working_hours)
    if busy_info.calendar_events is None:
        continue
    for event in busy_info.calendar_events:
        print("busy_type:", event.busy_type, "start:", event.start)
