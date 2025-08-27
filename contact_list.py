from exchangelib import Credentials, Account, Configuration, NTLM, BASIC, DIGEST
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib.indexed_properties import PhoneNumber

# Suppress only the InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)

# Set the HTTP adapter to use the custom RootCAAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('YODA_EMAIL_ADDRESS')
email_address = os.getenv('YODA_EMAIL_ADDRESS')
password = os.getenv('YODA_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server,
                       credentials=credentials, 
                      # auth_type=BASIC,
                      # auth_type=NTLM,
)
account = Account(primary_smtp_address=email_address,
                  config=config, access_type='delegate')

print(account.inbox.name)
print(config.auth_type)
# List all contacts
print("Searching for contacts with phone number: +1-555-555-5550")
print("-" * 50)

phone_number = "+1-555-555-5550"
found_contacts = []

# Method 1: Filter contacts that have phone numbers and then check the content
# Note: exchangelib doesn't support direct phone number content filtering in queries
# So we need to fetch contacts and filter locally
contacts_with_phones = account.contacts.filter(
    phone_numbers__exists=True
).all()

for contact in contacts_with_phones:
    if hasattr(contact, 'phone_numbers') and contact.phone_numbers:
        for phone in contact.phone_numbers:
            if phone_number in str(phone.phone_number):
                found_contacts.append(contact)
                break

# Method 2: Alternative approach - check all contacts for any phone field containing the number
if not found_contacts:
    print("No contacts found with phone_numbers field, checking all contacts...")
    for contact in account.contacts.all():
        # Check various phone number fields
        phone_found = False
        
        # Check phone_numbers indexed property
        if hasattr(contact, 'phone_numbers') and contact.phone_numbers:
            for phone in contact.phone_numbers:
                if phone_number in str(phone.phone_number):
                    phone_found = True
                    break
        
        # Check individual phone fields
        if not phone_found and hasattr(contact, 'business_phone') and contact.business_phone:
            if phone_number in str(contact.business_phone):
                phone_found = True
        
        if not phone_found and hasattr(contact, 'mobile_phone') and contact.mobile_phone:
            if phone_number in str(contact.mobile_phone):
                phone_found = True
                
        if not phone_found and hasattr(contact, 'home_phone') and contact.home_phone:
            if phone_number in str(contact.home_phone):
                phone_found = True
        
        if phone_found:
            found_contacts.append(contact)

# Display results
if found_contacts:
    print(f"Found {len(found_contacts)} contact(s) with phone number {phone_number}:")
    for contact in found_contacts:
        print(f"ID: {contact.id}")
        print(f"Display Name: {contact.display_name}")
        
        # Show all phone numbers for this contact
        if hasattr(contact, 'phone_numbers') and contact.phone_numbers:
            print("Phone Numbers:")
            for phone in contact.phone_numbers:
                print(f"  {phone.label}: {phone.phone_number}")
        
        if hasattr(contact, 'business_phone') and contact.business_phone:
            print(f"Business Phone: {contact.business_phone}")
        if hasattr(contact, 'mobile_phone') and contact.mobile_phone:
            print(f"Mobile Phone: {contact.mobile_phone}")
        if hasattr(contact, 'home_phone') and contact.home_phone:
            print(f"Home Phone: {contact.home_phone}")
        print("-" * 30)
else:
    print(f"No contacts found with phone number {phone_number}")