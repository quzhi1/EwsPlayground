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

# Print the events
print("Primary calendar events:")
for item in calendar_items:
    if isinstance(item, CalendarItem):
        print("subject:", item.subject, "start:", item.start)

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
        print("subject:", item.subject, "start:", item.start)