from exchangelib import Credentials, Account, Configuration
from exchangelib.folders import FolderCollection, SingleFolderQuerySet
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

for f in FolderCollection(account=account, folders=[account.root]).find_folders():
    try:
        f_or_error = SingleFolderQuerySet(account=account, folder=f).resolve()
    except Exception as e:
        print(f"ERROR: GetFolder on folder {f} failed: {e}")
    if isinstance(f_or_error, Exception):
        print(f"ERROR: GetFolder on folder {f} returned error: {f_or_error}")
