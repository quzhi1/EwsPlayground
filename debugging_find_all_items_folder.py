from exchangelib import Credentials, Account, Configuration
import os

# exchange_server = 'east.EXCH092.serverdata.net'
# username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
# password = os.getenv('INTERMEDIA_PASSWORD')
exchange_server = 'exch.myexchangeemail.com'
username = os.getenv('MYEXCHANGEEMAIL_EMAIL_ADDRESS')
password = os.getenv('MYEXCHANGEEMAIL_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

print(account.root / 'AllItems')
