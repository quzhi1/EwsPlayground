from exchangelib import Credentials, Account, Configuration
from exchangelib.folders import SingleFolderQuerySet, BaseFolder
from exchangelib.properties import DistinguishedFolderId
import os
from typing import List, Optional

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')

credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

def get_folders_paged(distinguished_folder_id: str, folder_classes: List[str], page_size: int=50, offset: int=0) -> tuple[List[BaseFolder], Optional[int]]:
    # Find folder by distinguished folder id
    parent_folder = SingleFolderQuerySet(
        account=account,
        folder=DistinguishedFolderId(
            id=distinguished_folder_id,
        ),
    ).resolve()
    
    index = 0
    progress = 0
    result = []
    for folder in parent_folder.walk():
        if folder.folder_class in folder_classes:
            if index >= offset:
                progress += 1
                result.append(folder)
                if progress >= page_size:
                    break
            index += 1
    if len(result) < page_size:
        return result, None
    return result, index + 1


# List all mail folders
print("Mail folders:")
offset = 0
while True:
    if offset is None:
        break
    print("offset ", offset)
    folders, offset = get_folders_paged("msgfolderroot", ["IPF.Note"], page_size=2, offset=offset)
    if not folders:
        break
    for folder in folders:
        print("\t\t" + folder.name + ": " + folder.id)

# List all secondary calendars
print("Secondary calendars:")
offset = 0
while True:
    if offset is None:
        break
    print("offset ", offset)
    folders, offset = get_folders_paged("calendar", ["IPF.Appointment"], page_size=2, offset=offset)
    if not folders:
        break
    for folder in folders:
        print("\t\t" + folder.name + ": " + folder.id)