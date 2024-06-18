from exchangelib import Credentials, Account, Configuration, EWSDateTime, EWSTimeZone, CalendarItem
from exchangelib.properties import UID
from exchangelib.extended_properties import ExtendedProperty
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

class GlobalObjectId(ExtendedProperty):
    distinguished_property_set_id = "Meeting"
    property_id = 3
    property_type = "Binary"


CalendarItem.register("global_object_id", GlobalObjectId)

# Find event by uid
uid = "040000008200E00074C5B7101A82E008000000009983D9D2A4C1DA0100000000000000001000000077D48B2F31EE2147B12CB9CE7FFAC178"
# uid = "abcde"
uid = UID.to_global_object_id(uid)
event = account.calendar.all().get(global_object_id=uid)
print("Event by uid:", event.subject, event.start, event.id)
