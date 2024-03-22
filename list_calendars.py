from exchangelib import Credentials, Account, Configuration
import os

# Replace these variables with your Exchange server settings
exchange_server = 'east.EXCH092.serverdata.net'
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')

credentials = Credentials(username=username, password=password)
config = Configuration(server=exchange_server, credentials=credentials, auth_type='basic')
account = Account(primary_smtp_address=username, autodiscover=False, config=config)

# List all calendars
primary_calendar = account.calendar
print('Primary Calendar:', primary_calendar)