from exchangelib import Credentials, Account, Configuration, CalendarItem
from exchangelib.properties import UID
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

# Find event by uid
uid = "040000008200E00074C5B7101A82E008000000009983D9D2A4C1DA0100000000000000001000000077D48B2F31EE2147B12CB9CE7FFAC178"
# uid = "abcde"

# EWS does not support filtering on field 'uid'

# items = account.calendar.filter(Q(uid=uid))
# for item in items:
#     print(f'Subject: {item.subject}')
#     print(f'Start: {item.start}')
#     print(f'End: {item.end}')
#     print(f'Location: {item.location}')
#     print(f'UID: {item.uid}')

uid = UID(UID.to_global_object_id(uid))
print("unhexlified uid:", uid)
event = account.calendar.all().only('global_object_id').get(global_object_id=uid)
print("Event by uid:", event.subject, event.start, event.id)

# for event in account.calendar.all().only("id", "uid"):
#     if isinstance(event, CalendarItem) and event.uid == uid:
#         print("subject:", event.subject, "start:", event.start, "id:", event.id)
