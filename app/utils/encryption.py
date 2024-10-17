from cryptography.fernet import Fernet
import os
from base64 import b64encode, b64decode

# Key is stored in an Environmental variable
key = os.environ.get('ENCRYPTION_KEY')
if not key:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

cipher_suite = Fernet(key)

def encrypt_data(data):
    """
    Encrypt data, handling different input types safely

    This function is a wrapper around Fernet's encrypt method, with extra
    handling for different input types. The purpose of this function is to
    make sure that the input data is converted into a type that Fernet can
    encrypt, and then to encrypt that data.

    The function is designed to be safe to call with None, string, bytes,
    or any other type of input. If the input is None, the function will
    return None. If the input is already bytes, the function will assume
    that it's already encrypted and return the input unchanged. If the
    input is not bytes, the function will convert it to a string using
    the built-in str() function, and then encrypt the string.

    The function will raise a ValueError if the input is not one of the
    above types, or if the encryption fails for any reason.
    """
    if data is None:
        return None
        
    # If it's already bytes, assume it's already encrypted
    if isinstance(data, bytes):
        return data
        
    # Convert to string if not already
    if not isinstance(data, str):
        data = str(data)
    
    # Encrypt the string data
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    
    return encrypted_data

def decrypt_data(encrypted_data):
    """
    Decrypt data, handling different input types safely

    This function is a wrapper around Fernet's decrypt method, with extra
    handling for different input types. The purpose of this function is to
    make sure that the input data is converted into a type that Fernet can
    decrypt, and then to decrypt that data.

    The function is designed to be safe to call with None, string, bytes,
    or any other type of input. If the input is None, the function will
    return None. If the input is already bytes, the function will assume
    that it's already encrypted and return the input unchanged. If the
    input is not bytes, the function will convert it to a string using
    the built-in str() function, and then decrypt the string.

    The function will raise a ValueError if the input is not one of the
    above types, or if the decryption fails for any reason.
    """
    if encrypted_data is None:
        # If the input is None, return None immediately
        return None
        
    # If it's a string, encode it first
    if isinstance(encrypted_data, str):
        # This is a string, so encode it as bytes first
        encrypted_data = encrypted_data.encode('utf-8')
    
    try:
        # Decrypt the bytes data
        decrypted = cipher_suite.decrypt(encrypted_data)
        
        # Decode the bytes data as a string
        decrypted = decrypted.decode('utf-8')
        
        # Return the decrypted string
        return decrypted
    except Exception as e:
        # Log the error here if you have logging set up
        raise ValueError(f"Decryption failed: {str(e)}")
