from exchangelib import Credentials, Account, Configuration
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

# List all calendars
for folder in account.msg_folder_root.walk():
    if folder.folder_class == 'IPF.Note':
        print("Folder Name:", folder.name)
        print("Folder ID:", folder.id)
