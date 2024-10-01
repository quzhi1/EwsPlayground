from exchangelib import Credentials, autodiscover
import os

username = os.getenv('INTERMEDIA_EMAIL_ADDRESS')
password = os.getenv('INTERMEDIA_PASSWORD')
cred = Credentials(username=username, password=password)
try:
    result, protocol = autodiscover.discover(username, cred)
    print("user_display_name:", result.user_settings['user_display_name'])
    print("smtp_address:", result.user_settings['auto_discover_smtp_address'])
    print("ews_supported_schemas:", result.user_settings['ews_supported_schemas'])
    print("service_endpoint:", protocol.config.service_endpoint)
    print("version.build:", protocol.config.version.build)
    print("version.api_version:", protocol.config.version.api_version)
    print("version.fullname:", protocol.config.version.fullname)
except Exception as e:
    print(e)
