from exchangelib import Credentials, Account, Configuration, Folder
import os

exchange_server = 'west.EXCH092.serverdata.net'
username = os.getenv('YODA_EMAIL_ADDRESS')
password = os.getenv('YODA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

def main():
    all_items_folder = find_all_items_folder(account)
    messages = all_items_folder.all().order_by('-datetime_received').only('subject', 'datetime_received', 'is_draft')

    for message in messages[0:10]:
        print('subject:', message.subject)
        print('datetime_received:', message.datetime_received)
        print('is_draft', message.is_draft)


def find_all_items_folder(account: Account) -> Folder:
    """
    Function to find and return the 'AllItems' folder under the root folder.
    
    :param account: The exchangelib Account object to search in.
    :return: The 'AllItems' folder if it exists, otherwise None.
    """
    # Walk through all subfolders under root and check for "AllItems"
    try:
        for folder in account.root.walk():
            if folder.name == 'AllItems':
                print("Found 'AllItems' folder")
                return folder
    except Exception:
        return None

    # Return None if the folder does not exist
    return None

if __name__ == '__main__':
    main()