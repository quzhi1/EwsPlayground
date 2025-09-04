from exchangelib import Credentials, Account, Configuration, ExtendedProperty, Message, Q
from exchangelib.folders import AllItems
from exchangelib.properties import ConversationId
from datetime import datetime, timezone
import os

exchange_server = 'Exchange2019.ionos.de'
username = os.getenv('IONOS_USERNAME')
email = os.getenv('IONOS_EMAIL_ADDRESS')
password = os.getenv('IONOS_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=email,
                  config=config, access_type='delegate')

class Flag(ExtendedProperty):
    property_tag = 0x1090
    property_type = 'Integer'

Message.register('flag', Flag)

NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME = [
    "id",
    "message_id",
    "conversation_id",
    "parent_folder_id",
    "subject",
    "in_reply_to",
    "author",
    "to_recipients",
    "cc_recipients",
    "bcc_recipients",
    "reply_to",
    "body",
    "attachments",
    "is_read",
    "flag",
    "is_draft",
    "has_attachments",
    "headers",
    "conversation_index",
    "datetime_received",
    "datetime_sent",
    "datetime_created",
    "last_modified_time",
    "item_class",
]

def main():
    all_items_folder = account.root.get_default_folder(AllItems)
    query = Q(datetime_received__lt=datetime.fromtimestamp(int(1752271200), tz=timezone.utc), datetime_received__gt=datetime.fromtimestamp(int(1752184800), tz=timezone.utc))
    print('--------------------------------')
    print('Using query:', query)
    messages = all_items_folder.filter(query).order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    for message in messages:
        print('id:', message.message_id)
        print('subject:', message.subject)
        print('datetime_received:', message.datetime_received)
    print('--------------------------------')
    print('Checking a certain message in range')
    messages = all_items_folder.filter(message_id='<bcfa1003ee7e4b448182f3e9037c633a@berlinovo.de>').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    for message in messages:
        print('id:', message.message_id)
        print('subject:', message.subject)
        print('datetime_received:', message.datetime_received)

if __name__ == '__main__':
    main()