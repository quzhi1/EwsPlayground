from exchangelib import Credentials, Account, Configuration, NTLM, BASIC, DIGEST
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

# Suppress only the InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)

# Set the HTTP adapter to use the custom RootCAAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('YODA_EMAIL_ADDRESS')
email = os.getenv('YODA_EMAIL_ADDRESS')
password = os.getenv('YODA_PASSWORD')
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