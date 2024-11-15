from exchangelib import Credentials, Account, Configuration
from typing import List
from exchangelib.folders import FolderCollection, SingleFolderQuerySet
from exchangelib.queryset import QuerySet
import os

exchange_server = 'exchange.homewatchcaregivers.com'
username = os.getenv('HOMEWATCHCAREGIVERS_EMAIL_ADDRESS')
password = os.getenv('HOMEWATCHCAREGIVERS_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')
message_id = '<!&!AAAAAAAAAAAYAAAAAAAAANnegKUYmgNFsvVHExaDAm7CgAAAGAAAAAAAAADZ3oClGJoDRbL1RxMWgwJuxII/AAEAAAAA@globalattendeehub.com>'

def main():
    messages = get_messages_with_same_id(account, message_id)
    num_messages = messages.count()
    if num_messages == 0:
        print('No messages found with message_id:', message_id)
        return
    for message in messages:
        print(f"Message found in folder {message.parent_folder_id} with subject {message.subject}")

def get_message_folders(account: Account) -> List[SingleFolderQuerySet]:
    top_folder = account.msg_folder_root
    email_folders = []
    for f in top_folder.walk():
        if f.CONTAINER_CLASS != 'IPF.Note':
            continue
        if account.drafts is not None and f.id == account.drafts.id:
            continue
        email_folders.append(f)
    return email_folders

def get_messages_with_same_id(account: Account, message_id: str) -> QuerySet:
    email_folders = get_message_folders(account)
    collection = FolderCollection(
        account=account, folders=email_folders)
    messages = collection.filter(message_id=message_id)
    return messages

if __name__ == '__main__':
    main()