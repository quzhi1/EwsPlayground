from exchangelib import Credentials, Account, Configuration
from exchangelib.folders import AllItems
import os

exchange_server = 'west.EXCH092.serverdata.net'
username = os.getenv('YODA_EMAIL_ADDRESS')
password = os.getenv('YODA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

def main():
    all_items_folder = account.root.get_default_folder(AllItems)
    messages = all_items_folder.all().order_by('-datetime_received').only('subject', 'datetime_received', 'is_draft')

    for message in messages[0:10]:
        print('subject:', message.subject)
        print('datetime_received:', message.datetime_received)
        print('is_draft', message.is_draft)


if __name__ == '__main__':
    main()