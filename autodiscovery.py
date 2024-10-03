from exchangelib import Credentials, autodiscover, Configuration, Account, NTLM, BASIC, DIGEST
from exchangelib.errors import UnauthorizedError, TransportError
import os

username = os.getenv('OVH_EMAIL_ADDRESS')
password = os.getenv('OVH_PASSWORD')
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

    for auth_type in [NTLM, BASIC, DIGEST]:
        server_endpoint_without_scheme = protocol.config.service_endpoint.split('://')[1]
        config = Configuration(
            server=server_endpoint_without_scheme,
            credentials=cred,
            auth_type=auth_type,
            # retry_policy=FaultTolerance(
            #     max_wait=os.getenv('EWS_TIMEOUT', 10),
            # ),
        )
        try:
            exlib_account = Account(
                primary_smtp_address=username, config=config, access_type='delegate')
            print(auth_type)
            break
        except (UnauthorizedError, TransportError):
            continue

except Exception as e:
    print(e)

