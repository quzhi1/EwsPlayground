from exchangelib import Credentials, Account, Configuration
from exchangelib.folders import AllItems
import os

exchange_server = 'exchange2019.ionos.com'
username = os.getenv('IONOS_EMAIL_ADDRESS')
email = os.getenv('IONOS_EMAIL_ADDRESS')
password = os.getenv('IONOS_PASSWORD')

credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=email,
                  config=config, access_type='delegate')

# Method 1: Find by distinguished folder id
all_items = account.root.get_default_folder(AllItems)
print(f"Folder ID: {all_items.id}")
print(f"Folder Name: {all_items.name}")

