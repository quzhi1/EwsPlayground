from exchangelib import Credentials, Account, Configuration
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

# Suppress only the InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)

# Set the HTTP adapter to use the custom RootCAAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

# exchange_server = 'autodiscover.rosellilaw.com'
# email = os.getenv('ROSELLILAW_EMAIL_ADDRESS')
# username = 'Rosellilaw\\rmroselli'
# password = os.getenv('ROSELLILAW_PASSWORD')
# exchange_server = 'webmail.wolve.com'
# username = os.getenv('WOLVE_EMAIL_ADDRESS')
# email = os.getenv('WOLVE_EMAIL_ADDRESS')
# password = os.getenv('WOLVE_PASSWORD')
exchange_server = 'mail.papara.com'
username = os.getenv('PAPARA_EMAIL_ADDRESS')
email = os.getenv('PAPARA_EMAIL_ADDRESS')
password = os.getenv('PAPARA_PASSWORD')
print(username, email, password)
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server,
                       credentials=credentials, 
                    #    auth_type=NTLM,
)
account = Account(primary_smtp_address=email,
                  config=config, access_type='delegate')

print(account.inbox.name)