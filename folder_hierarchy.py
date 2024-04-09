from exchangelib import Credentials, Account, Configuration
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')

credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username, config=config, access_type='delegate')

def print_folder_hierarchy(folder, indent=0):
    print('  ' * indent + folder.name)
    for child_folder in folder.children:
        print_folder_hierarchy(child_folder, indent+1)

print_folder_hierarchy(account.root)