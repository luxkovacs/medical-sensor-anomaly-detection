"""
Module for handling encryption and decryption of sensitive data.
"""
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# This is just a development key - in production, use environment variables
_DEFAULT_KEY = b'this_is_a_default_key_for_development_only'
_SALT = b'static_salt_for_development_only'

def _get_key(password=None):
    """Derive an encryption key from a password or use default key."""
    if password is None:
        password = _DEFAULT_KEY
        
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=100000,
    )
    
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt(data, password=None):
    """Encrypt the provided data."""
    if isinstance(data, str):
        data = data.encode('utf-8')
        
    key = _get_key(password)
    f = Fernet(key)
    return f.encrypt(data)

def decrypt(encrypted_data, password=None):
    """Decrypt the provided data."""
    key = _get_key(password)
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')
