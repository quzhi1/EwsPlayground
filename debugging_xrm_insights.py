from exchangelib.folders import FolderCollection
from exchangelib.util import PrettyXmlHandler
from exchangelib import Credentials, Account, Configuration
import os
import logging

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

logging.basicConfig(level=logging.DEBUG, handlers=[PrettyXmlHandler()])
for f in FolderCollection(account=account, folders=[account.root]).find_folders():
    if f.name != "XrmInsights":
        continue
    fc = FolderCollection(account=account, folders=[f])
    additional_fields = fc.get_folder_fields(target_cls=fc._get_target_cls())
    list(fc.get_folders(additional_fields=set()))
    for field in additional_fields:
        try:
            list(fc.get_folders(additional_fields={field}))
        except Exception as e:
            print(f"ERROR: GetFolder with field {field!r} failed: {e!r}")
    list(fc.get_folders(additional_fields=additional_fields))