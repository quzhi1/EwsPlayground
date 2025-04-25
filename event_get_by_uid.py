from exchangelib import Credentials, Account, Configuration, CalendarItem
from exchangelib.extended_properties import ExtendedProperty
from exchangelib.properties import UID
import os
import base64

def main():
    # Exchange server configuration
    exchange_server = 'mail.cornerstonestaffing.com'
    email_address = os.getenv('CORNERSTONE_EMAIL_ADDRESS')
    username = os.getenv('CORNERSTONE_USERNAME')
    password = os.getenv('CORNERSTONE_PASSWORD')
    event_id = "AAMkADU0NTZkN2JiLTI5OTYtNGUyZi04NzlhLTg4ZTA1MGE2ZTE5ZQBGAAAAAABUpPfKnta8TrgKs8hCQd1RBwBsAyEWXY6/RL25MGl/PmSNAAAAAAENAABsAyEWXY6/RL25MGl/PmSNAAMzSgXYAAA="
    run_test(exchange_server, email_address, username, password, event_id)

    exchange_server = 'east.EXCH092.serverdata.net'
    email_address = os.getenv('YODA_EMAIL_ADDRESS')
    username = os.getenv('YODA_EMAIL_ADDRESS')
    password = os.getenv('YODA_PASSWORD')
    event_id = "AAMkADZhMzdkMDEzLWU1YTgtNDdiOC04ZmY4LTA4NWIzY2YzZTY1NQBGAAAAAADoKPQ9PfObQLWKHSb9UK7cBwCT/uDqRbzaRZLQpdxtY0TGAAAAAAENAACT/uDqRbzaRZLQpdxtY0TGAAPg7BhbAAA="
    run_test(exchange_server, email_address, username, password, event_id)

class GlobalObjectId(ExtendedProperty):
    distinguished_property_set_id = "Meeting"
    property_id = 3
    property_type = "Binary"

# Register the property with CalendarItem
CalendarItem.register("global_object_id", GlobalObjectId)

def detect_uid_format(uid):
    """
    Detects the format of a UID string. So far we have only found 'exchange' and 'hex' formats.

    Returns:
        'exchange' - Exchange format (hex string with specific header)
        'uuid' - Standard UUID format (8-4-4-4-12)
        'hex' - Simple hex string format (32 chars)
        'base64' - Base64 encoded format
        'hex_without_dashes' - Hex string without dashes (32 chars)
        'hex_with_dashes' - Hex string with dashes (36 chars)
        'unknown' - Unknown format
    """
    if not isinstance(uid, str):
        return 'unknown'
        
    # Check if it's an Exchange format UID
    # Exchange UIDs start with '040000008200E00074C5B7101A82E008'
    if uid.startswith('040000008200E00074C5B7101A82E008'):
        return 'exchange'
    
    # Check if it's a UUID format
    # UUIDs are in the format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    if len(uid) == 36 and uid.count('-') == 4:
        parts = uid.split('-')
        if (len(parts[0]) == 8 and len(parts[1]) == 4 and 
            len(parts[2]) == 4 and len(parts[3]) == 4 and 
            len(parts[4]) == 12):
            return 'uuid'
    
    # Check if it's a simple hex string (like da4085abb02e4c62b6366c4e1b548e83)
    if len(uid) == 32 and all(c in '0123456789abcdef' for c in uid.lower()):
        return 'hex'
    
    # Check if it's a hex string with dashes (like da4085ab-b02e-4c62-b636-6c4e1b548e83)
    if len(uid) == 36 and uid.count('-') == 4:
        hex_parts = uid.split('-')
        if all(len(part) in [8, 4] and all(c in '0123456789abcdef' for c in part.lower()) for part in hex_parts):
            return 'hex_with_dashes'
    
    # Check if it's a base64 encoded string
    try:
        # Try to decode as base64
        decoded = base64.b64decode(uid)
        return 'base64'
    except:
        pass
    
    return 'unknown'

def normalize_uid(uid, format_type):
    """
    Normalizes a UID to a standard format for GlobalObjectId creation.
    
    Args:
        uid (str): The UID string to normalize
        format_type (str): The detected format of the UID
        
    Returns:
        str: The normalized UID in hex format without dashes
    """
    if format_type == 'uuid':
        # Remove dashes from UUID
        return uid.replace('-', '')
    elif format_type == 'hex_with_dashes':
        # Remove dashes from hex string
        return uid.replace('-', '')
    elif format_type == 'base64':
        # Convert base64 to hex
        decoded = base64.b64decode(uid)
        return decoded.hex()
    elif format_type == 'exchange':
        # For exchange format, we'll use it as is
        return uid
    elif format_type == 'hex':
        # Already in correct format
        return uid
    else:
        raise ValueError(f"Unsupported UID format: {format_type}")

def create_global_object_id(uid):
    """
    Creates a GlobalObjectId from a UID string, matching the exact format used by Exchange.
    
    The GlobalObjectId is a binary structure that Exchange uses to uniquely identify calendar items.
    This function creates a byte sequence that exactly matches what Exchange generates.
    
    Args:
        uid (str): The UID string to convert
        
    Returns:
        bytes: The GlobalObjectId in binary format
    """
    # Detect the format of the UID
    format_type = detect_uid_format(uid)
    
    # Normalize the UID to a standard format
    normalized_uid = normalize_uid(uid, format_type)
    
    if format_type == 'exchange':
        # For exchange format, use the UID directly
        return bytes.fromhex(normalized_uid)
    elif format_type == 'hex':
        # For hex format, create the standard GlobalObjectId structure
        uid_bytes = normalized_uid.encode('ascii')
        # This is the standard GlobalObjectId structure for Exchange.
        # It is a binary structure that Exchange uses to uniquely identify calendar items.
        # The structure is as follows:
        # 040000008200e00074c5b7101a82e00800000000000000000000000000000000000000002d0000007643616c2d55696401000000
        # The first 16 bytes are the same for all GlobalObjectIds.
        # The next 16 bytes are the UID of the calendar item, encoded with the ASCII character set.
        # The last 2 bytes are the length of the UID.
        prefix = bytes.fromhex('040000008200e00074c5b7101a82e00800000000000000000000000000000000000000002d0000007643616c2d55696401000000')
        suffix = bytes.fromhex('00')
        return prefix + uid_bytes + suffix
    else:
        # For other formats, use the exchangelib's built-in conversion
        return UID.to_global_object_id(uid)

def run_test(exchange_server, email_address, username, password, event_id):
    # Set up connection
    credentials = Credentials(username=username, password=password)
    config = Configuration(server=exchange_server, credentials=credentials)
    account = Account(primary_smtp_address=email_address,
                    config=config, access_type='delegate')

    # First, get the event by its ID
    event = account.calendar.all().get(id=event_id)

    # Get the event's original UID and detect its format
    print("Original UID:", event.uid)
    uid_format = detect_uid_format(event.uid)
    print("UID format:", uid_format)

    # Create GlobalObjectId
    created_goid = create_global_object_id(event.uid)

    print("Created GlobalObjectId (raw):", created_goid)
    print("Created GlobalObjectId (hex):", created_goid.hex())
    print("Created GlobalObjectId (base64):", base64.b64encode(created_goid).decode())

    # Try to find the event using our created GlobalObjectId
    try:
        found_event = account.calendar.all().get(global_object_id=created_goid)
        print("\nFound event using created GlobalObjectId:")
        print("Subject:", found_event.subject)
        print("Start:", found_event.start)
        print("ID:", found_event.id)
        print("UID:", found_event.uid)
    except Exception as e:
        print(f"\nError finding event: {str(e)}")

if __name__ == "__main__":
    main()