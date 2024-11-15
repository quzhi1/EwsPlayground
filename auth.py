from exchangelib import Credentials, Account, Configuration, NTLM
import os

exchange_server = 'autodiscover.rosellilaw.com'
email = os.getenv('ROSELLILAW_EMAIL_ADDRESS')
username = 'Rosellilaw\\rmroselli'
password = os.getenv('ROSELLILAW_PASSWORD')
print(username, email, password)
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server,
                       credentials=credentials, 
                    #    auth_type=NTLM,
                       )
account = Account(primary_smtp_address=email,
                  config=config, access_type='delegate')

print(account.inbox.name)