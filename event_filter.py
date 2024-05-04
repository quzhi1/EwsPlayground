from exchangelib import Credentials, Account, Configuration, EWSDateTime, EWSTimeZone, CalendarItem
from datetime import datetime, timedelta
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

# Find event by uid
uid = "040000008200E00074C5B7101A82E008000000007FB4D296AA9DDA010000000000000000100000002BAD9240C65B9440AD614916D81C3D72"
event = account.calendar.get(uid=uid)
print("Event by uid:", event.subject, event.start, event.id)
# EWS does not support filtering on field 'uid'
