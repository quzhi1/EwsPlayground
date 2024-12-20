from exchangelib import Credentials, Account, Configuration
import os

# exchange_server = 'east.EXCH092.serverdata.net'
# username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
# password = os.getenv('INTERMEDIA_PASSWORD')
# exchange_server = 'exch.myexchangeemail.com'
# username = os.getenv('MYEXCHANGEEMAIL_EMAIL_ADDRESS')
# password = os.getenv('MYEXCHANGEEMAIL_PASSWORD')
exchange_server = 'webmail.mollundpunt.at'
username = os.getenv('MOLLUNDPUNT_USERNAME')
email = os.getenv('MOLLUNDPUNT_EMAIL_ADDRESS')
password = os.getenv('MOLLUNDPUNT_PASSWORD')
print(username, email, password)
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=email,
                  config=config, access_type='delegate')

# print(account.root / 'AllItems')
for folder in account.msg_folder_root.walk():
    print('name:', folder.name)
    print('container_class:', folder.CONTAINER_CLASS)
    print('id:', folder.id)
