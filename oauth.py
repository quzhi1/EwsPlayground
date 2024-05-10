from exchangelib import Account, OAuth2Credentials, Configuration

# These values are obtained from your Azure app registration
client_id = 'your-client-id'
client_secret = 'your-client-secret'  # Needed only for confidential clients
tenant_id = 'your-tenant-id'
# Token obtained through OAuth2
access_token = 'your-access-token'

credentials = OAuth2Credentials(
    client_id=client_id,
    client_secret=client_secret,  # Omit if using a public client
    tenant_id=tenant_id,
    identity=access_token  # The access token
)

# Set up the configuration for the account
config = Configuration(credentials=credentials, server='outlook.office365.com')

# Initialize the account
account = Account(primary_smtp_address='your-email@example.com', config=config, autodiscover=False, access_type='delegate')