from exchangelib import Credentials, Account, Configuration, Folder
from exchangelib.items import Message
import os

ALL_ITEMS_FOLDER = 'AllItems'
limit = 1
offset = 0

def main():
    exchange_server = 'west.exch090.serverdata.net'
    username = os.getenv('SALESLOFT_USERNAME')
    email = os.getenv('SALESLOFT_EMAIL_ADDRESS')
    password = os.getenv('SALESLOFT_PASSWORD')
    credentials = Credentials(username=username, password=password)
    config = Configuration(server=exchange_server, credentials=credentials)
    account = Account(primary_smtp_address=email, config=config, access_type='delegate')

    all_items_folder = find_all_items_folder(account)
    messages = all_items_folder.all().order_by('-datetime_received')
    num_messages = messages.count()
    conversation_ids = []
    
    i = 0
    while len(conversation_ids) < limit and offset + i < num_messages: # this condition checks if we have enough conversations to return or if we have reached the end of the messages
        for message in messages[offset + i:offset + i + limit]: # we page by limit instead of limit - len(conversation_ids) because we want to avoid situations where we're strict paging because of only one thread
            if offset + i >= num_messages or len(conversation_ids) >= limit:
                break

            i += 1
            if not has_message_id(message): # exclude messages that don't have a message_id header
                continue
            if message.conversation_id.id in conversation_ids: 
                continue
            if message.is_draft: # exclude drafts
                continue
            conversation_ids.append(message.conversation_id.id)

    # conversation_ids = [encode_str(c) for c in conversation_ids]
    next_offset = offset + i if num_messages > offset + i else None
    print(conversation_ids, next_offset)

def find_all_items_folder(account: Account) -> Folder:
    """
    Function to find and return the 'AllItems' folder under the root folder.
    
    :param account: The exchangelib Account object to search in.
    :return: The 'AllItems' folder if it exists, otherwise None.
    """
    # Walk through all subfolders under root and check for "AllItems"
    try:
        for folder in account.root.walk():
            if folder.name == ALL_ITEMS_FOLDER:
                return folder
    except Exception:
        return None

    # Return None if the folder does not exist
    return None

def has_message_id(item: Message) -> bool:
    try:
        return item.message_id is not None and item.message_id != ""
    except AttributeError:
        return False

if __name__ == '__main__':
    main()