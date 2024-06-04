from exchangelib import Credentials, Account, Configuration, EWSDate, EWSDateTime, EWSTimeZone, CalendarItem, Attendee, Mailbox
from datetime import datetime
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

# Create a new calendar event
event = CalendarItem(
    account=account,
    folder=account.calendar,
    subject="Test event from python script",
    start=EWSDate.from_string('2024-06-05'),
    end=EWSDate.from_string('2024-06-05'),
    body="This is a test event created from a python script",
    location="New York",
)
event.save()
print("Created event:", event.subject, "id:", event.id, "start:", event.start, "end:", event.end)

now = datetime.now()
start = EWSDateTime(now.year, now.month, now.day, 8, 0, 0,
                    tzinfo=EWSTimeZone("Europe/Copenhagen"))
end = EWSDateTime(now.year, now.month, now.day, 9, 0, 0,
                  tzinfo=EWSTimeZone("Europe/Copenhagen"))
event.start = start
event.end = end
event.save()
print("Updated event:", event.subject, "id:", event.id, "start:", event.start, "end:", event.end)
