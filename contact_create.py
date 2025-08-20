from exchangelib import Credentials, Account, Configuration
from exchangelib.indexed_properties import PhoneNumber
from exchangelib import Contact
import os

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('YODA_EMAIL_ADDRESS')
email_address = os.getenv('YODA_EMAIL_ADDRESS')
password = os.getenv('YODA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=email_address, config=config, access_type='delegate')

# Create a new contact
new_contact = Contact(
    account=account,
    folder=account.contacts,
    display_name='Test script',
    given_name='Test script',
    phone_numbers=[
        PhoneNumber(phone_number='1234567890', label='HomePhone'),
        PhoneNumber(phone_number='1234567891', label='BusinessPhone'),
        PhoneNumber(phone_number='1234567892', label='BusinessPhone'), # This will override the previous one because it is duplicate
    ],
)
new_contact.save()
print(f"Contact created: {new_contact.id}")
new_contact.refresh()
print(f"Contact refreshed: {new_contact}")