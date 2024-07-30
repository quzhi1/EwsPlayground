from exchangelib import Credentials, autodiscover
import os

# username = os.getenv('EWS_OVH_USERNAME')
# password = os.getenv('EWS_OVH_PASSWORD')
username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
cred = Credentials(username=username, password=password)
try:
    result, protocol = autodiscover.discover(username, cred)
    print("user_display_name:", result.user_settings['user_display_name'])
    print("smtp_address:", result.user_settings['auto_discover_smtp_address'])
    print("ews_supported_schemas:", result.user_settings['ews_supported_schemas'])
    print("service_endpoint:", protocol.config.service_endpoint)
    print("version:", protocol.config.version)
except Exception as e:
    print(e)
