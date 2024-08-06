from exchangelib import Credentials, Account, Configuration, Version, Build as _Build

import os
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('exchangelib').setLevel(logging.DEBUG)
logging.getLogger('requests').setLevel(logging.DEBUG)


class Build(_Build):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except ValueError:
            pass

# exchange_server = 'ex.mail.ovh.ca'
# username = os.getenv('EWS_OVH_USERNAME')
# password = os.getenv('EWS_OVH_PASSWORD')
exchange_server = 'zimbra.immo-facile.com'
username = os.getenv('EWS_IMMO_USERNAME')
password = os.getenv('EWS_IMMO_PASSWORD')
credentials = Credentials(
    username=username,
    password=password,
)
config = Configuration(
    server=exchange_server,
    credentials=credentials,
    # Add version hint to skip version guessing routines
    version=Version(
        api_version="Version366750107",
        build=Build(
            major_version=-1102247790,
            minor_version=-801581130,
            major_build=-1919954918,
            minor_build=-880192749,
        ),
    ),
)
account = Account(
    primary_smtp_address=username,
    config=config,
    access_type='delegate',
    # Disable autodiscover to skip version guessing routines
    autodiscover=False,
)

print("Primary Calendar Name:", account.calendar.name)
