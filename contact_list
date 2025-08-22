from exchangelib import Credentials, Account, Configuration, NTLM, BASIC, DIGEST
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

# Suppress only the InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)

# Set the HTTP adapter to use the custom RootCAAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

exchange_server = 'mail.ypicrew.com'
username = os.getenv('YPICREW_USERNAME')
email = os.getenv('YPICREW_EMAIL_ADDRESS')
password = os.getenv('YPICREW_PASSWORD')
print(username, email, password)
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server,
                       credentials=credentials, 
                      # auth_type=BASIC,
                      # auth_type=NTLM,
)
account = Account(primary_smtp_address=email,
                  config=config, access_type='delegate')

print(account.inbox.name)
print(config.auth_type)
# List all contacts
limit = 3
for contact in account.contacts.all():
    print(contact.id, contact.display_name)
    limit -= 1
    if limit <= 0:
        break