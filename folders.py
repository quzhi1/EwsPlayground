from exchangelib import Credentials, Account, Configuration
import os

exchange_server = 'webmail.wb-duisburg.de'
username = os.getenv('DUISBURG_EMAIL_ADDRESS')
password = os.getenv('DUISBURG_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

# List all message folders
for folder in account.msg_folder_root.walk():
    if folder.folder_class == 'IPF.Note':
        print("Folder Name:", folder.name)
        print("Folder ID:", folder.id)
