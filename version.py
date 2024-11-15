from exchangelib import Credentials, Account, Configuration, Version, Build
from exchangelib.properties import DistinguishedFolderId, Mailbox
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

account.version = Version(build=Build(15, 1, 2507, 39),
                          api_version="Exchange2016")
distinguished_folders = [
    cls(
        _distinguished_id=DistinguishedFolderId(
            id=cls.DISTINGUISHED_FOLDER_ID,
            mailbox=Mailbox(email_address=account.primary_smtp_address),
        ),
        root=account.root,
    )
    for cls in account.root.WELLKNOWN_FOLDERS
    if cls.get_folder_allowed and cls.supports_version(account.version)
]
print(sorted([f.DISTINGUISHED_FOLDER_ID for f in distinguished_folders]))
