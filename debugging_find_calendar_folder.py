from exchangelib import Credentials, Account, Configuration, Mailbox
from exchangelib.folders import SingleFolderQuerySet
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
        mailbox=Mailbox(
            email_address=account.primary_smtp_address,
        ),
    ),
).resolve()
print("folder name:", folder.name)
