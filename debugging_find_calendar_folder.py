from exchangelib import Credentials, Account, Configuration, Folder
from exchangelib.folders import SingleFolderQuerySet, Calendar
from exchangelib.properties import DistinguishedFolderId
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

folder = SingleFolderQuerySet(
    account=account,
    folder=DistinguishedFolderId(
        id='calendar',
    ),
).resolve()
print("folder name:", folder.name)
