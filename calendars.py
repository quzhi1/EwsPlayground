from exchangelib import Credentials, Account, Configuration, Folder
from exchangelib.folders import SingleFolderQuerySet, Calendar
from exchangelib.properties import DistinguishedFolderId
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

# List all calendars
python_created_calendar_id = None
print("Primary Calendar Name:", account.calendar.name)
print("Primary Calendar ID:", account.calendar.id)
for folder in account.calendar.walk():
    if folder.folder_class == 'IPF.Appointment':
        print("Secondary Calendar Name:", folder.name)
        print("Secondary Calendar ID:", folder.id)
        if folder.name == "python created" or folder.name == "python created renamed":
            python_created_calendar_id = folder.id

# Create calendar
if python_created_calendar_id is None:
    new_calendar = Folder(parent=account.calendar, name="python created", folder_class='IPF.Appointment')
    new_calendar.save()
    python_created_calendar_id = new_calendar.id
    print("Created calendar, name:", new_calendar.name, "ID:", new_calendar.id)

# Find calendar by id
find_folder_result = SingleFolderQuerySet(
    account=account,
    folder=account.calendar,
).get(id=python_created_calendar_id)
print("Find folder by id result:", find_folder_result.name)

# Find calendar by distinguished folder id
find_folder_by_distinguished_folder_id_result = SingleFolderQuerySet(
    account=account,
    folder=DistinguishedFolderId(
        id=Calendar.DISTINGUISHED_FOLDER_ID,
    ),
).resolve()
print(
    "Find folder by distinguished folder id result:",
    find_folder_by_distinguished_folder_id_result.name,
    "folder_class:",
    find_folder_by_distinguished_folder_id_result.folder_class,
)

# Rename calendar
find_folder_result.name = "python created renamed"
find_folder_result.save(update_fields=['name'])
print("Folder renamed")

# Delete calendar
find_folder_result.delete()
print("Folder deleted")