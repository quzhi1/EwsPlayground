from exchangelib import Credentials, Account, Configuration, CalendarItem
from exchangelib.properties import UID
from exchangelib.extended_properties import ExtendedProperty
import os
import uuid

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
uid = "040000008200E00074C5B7101A82E0080000000069E26FC662C6DA01000000000000000010000000E912B5F2D12C544FADE443C0D0C6E3EE"
# uid = "abcde"
uid = UID.to_global_object_id(uid)
event = account.calendar.all().get(global_object_id=uid)
print("Subject:", event.subject, "start:", event.start, "id:",
      event.id, "uid:", event.uid)
