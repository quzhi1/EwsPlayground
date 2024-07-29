from exchangelib import Credentials, Account, Configuration
import os
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('exchangelib').setLevel(logging.DEBUG)
logging.getLogger('requests').setLevel(logging.DEBUG)

exchange_server = 'ex.mail.ovh.ca'
username = os.getenv('EWS_OVH_USERNAME')
password = os.getenv('EWS_OVH_PASSWORD')
credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials)
account = Account(primary_smtp_address=username,
                  config=config, access_type='delegate')

print("Primary Calendar Name:", account.calendar.name)
