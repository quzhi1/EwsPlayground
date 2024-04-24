from exchangelib import Credentials, Account, Configuration, EWSDateTime, EWSTimeZone, CalendarItem, Attendee, Mailbox
from exchangelib.fields import MONDAY, WEDNESDAY
from exchangelib.recurrence import Recurrence, WeeklyPattern
from datetime import datetime
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

# Create a new calendar event
now = datetime.now()
start = EWSDateTime(now.year, now.month, now.day, 8, 0, 0, tzinfo=EWSTimeZone("Europe/Copenhagen"))
end = EWSDateTime(now.year, now.month, now.day, 9, 0, 0, tzinfo=EWSTimeZone("Europe/Copenhagen"))
event = CalendarItem(
    account=account,
    folder=account.calendar,
    subject="Test event from python script",
    start=start,
    end=end,
    body="This is a test event created from a python script",
    location="New York",
    required_attendees=[
        Attendee(
            mailbox=Mailbox(
                name="Zhi Live",
                email_address="quzhi65222714@live.com",
            ),
        ),
        Attendee(
            mailbox=Mailbox(
                name="Zhi Gmail",
                email_address="quzhi65222714@gmail.com",
            ),
        )
    ],
    reminder_minutes_before_start=15,
    recurrence=Recurrence(
        pattern=WeeklyPattern(interval=1, weekdays=[MONDAY, WEDNESDAY]),
        start=start.date(),
        number=7,
    ),
)
event.save()
print("Created event:", event.subject, "id:", event.id)

# Update the event
event.subject = "Updated test event from python script"
event.save()
print("Updated event:", event.subject, "id:", event.id)

# # Delete the event
event.delete()
print("Deleted event:", event.subject, "id:", event.id)
