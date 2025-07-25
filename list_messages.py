from exchangelib import Credentials, Account, Configuration, ExtendedProperty, Message, Q
from exchangelib.folders import AllItems
from exchangelib.properties import ConversationId
import os

exchange_server = 'mail.candraccounting.com'
username = os.getenv('CANDRACCOUNTING_USERNAME')
email = os.getenv('CANDRACCOUNTING_EMAIL_ADDRESS')
password = os.getenv('CANDRACCOUNTING_PASSWORD')
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
    # all_items_folder = account.root.get_default_folder(AllItems)
    # target_folder = None
    # for folder in account.msg_folder_root.walk():
    #     if folder.id == 'AQMkADZmOTkAN2M0ZC1hZmEwLTQ1MWUtYWY5MS00ZTNjNThiN2RiNGUALgAAA6xhWZabYYlIk3D4rxYJONIBADPIg/iUAhxBrdo2sykkLt0AAAIBWgAAAA==':
    #         target_folder = folder
    #         print('Target folder:', target_folder.id, target_folder.name, target_folder.CONTAINER_CLASS, target_folder.folder_class)
    #         break
    # if target_folder is None:
    #     print('Target folder not found')
    #     return
    # messages = all_items_folder.filter(item_class='IPM.Note').order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # messages = all_items_folder.all().order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # messages = account.inbox.all().order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # messages = all_items_folder.filter(Q(), is_draft=False, item_class='IPM.Note').order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # aqs = Q(author__icontains='zhi.q@nylas.com', has_attachments=False) & ~Q(flag=2)
    # query = aqs & Q(is_draft=False, item_class='IPM.Note')
    # query = query & Q(conversation_id=ConversationId(id='AAQkADZhMzdkMDEzLWU1YTgtNDdiOC04ZmY4LTA4NWIzY2YzZTY1NQAQAImvnrfwEytJmqMLIPVAUKM='))
    # query = Q(to_recipients__icontains='yoda@nylas.info')
    # query = "To:yoda@nylas.info"
    # query = "from:\"zhi.q@nylas.com\""
    query = Q(conversation_id=ConversationId(id='AAQkADQyOWY0MTJmLWZiNDktNDY1Zi1hY2I1LWMxYmY5MjhlZTQ0MgAQAPblIsQdm0xfo0uZiuONFnc='))
    # messages = all_items_folder.filter(query).order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # messages = account.inbox.filter(query).order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # messages = target_folder.filter(item_class='IPM.Note').order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # print('--------------------------------')
    # print('Using query:', query)
    # messages = all_items_folder.filter(query).order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    messages = account.inbox.filter(query).order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    for message in messages:
        print('id:', message.id)
        print('subject:', message.subject)
        print('conversation_id:', message.conversation_id)
        break
    print('--------------------------------')
    # print('Using native filter: author__icontains="zhi.q@nylas.com"')
    # messages = all_items_folder.filter(author__icontains='zhi.q@nylas.com').order_by('-datetime_received').only(*NECESSARY_MESSAGE_FIELDS_WITHOUT_MIME)
    # for message in messages:
    #     print('id:', message.id)
    #     print('subject:', message.subject)
    #     print('author:', message.author)
    #     print('sender:', message.sender)
    #     if hasattr(message, 'from_'):
    #         print('from:', message.from_)
    #     break

if __name__ == '__main__':
    main()