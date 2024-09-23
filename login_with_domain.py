from exchangelib import Credentials, Account, Configuration
from exchangelib.folders import FolderCollection, SingleFolderQuerySet
import os

exchange_server = 'ews.thementornetwork.com'
username = os.getenv('SEVITAHEALTH_USERNAME')
password = os.getenv('SEVITAHEALTH_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=os.getenv('SEVITAHEALTH_EMAIL_ADDRESS'),
                  config=config, access_type='delegate')

print(account.inbox.name)
