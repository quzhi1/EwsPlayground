from exchangelib import Credentials, Account, Configuration, ExtendedProperty, Message, Q
from exchangelib.folders import AllItems
from exchangelib.properties import ConversationId
import os

exchange_server = 'west.EXCH092.serverdata.net'
username = os.getenv('YODA_EMAIL_ADDRESS')
password = os.getenv('YODA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
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
    # messages = all_items_folder.filter(item_class='IPM.Note').order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # messages = all_items_folder.all().order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # messages = all_items_folder.filter(Q(), is_draft=False, item_class='IPM.Note').order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    aqs = Q(author__icontains='zhi.q@nylas.com', has_attachments=False) & ~Q(flag=2)
    query = aqs & Q(is_draft=False, item_class='IPM.Note')
    query = query & Q(conversation_id=ConversationId(id='AAQkADZhMzdkMDEzLWU1YTgtNDdiOC04ZmY4LTA4NWIzY2YzZTY1NQAQAImvnrfwEytJmqMLIPVAUKM='))
    messages = all_items_folder.filter(query).order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)

    for message in messages[0:10]:
        print('subject:', message.subject)
        print('sender', message.author.email_address)
        print('conversation_id', message.conversation_id.id)

if __name__ == '__main__':
    main()