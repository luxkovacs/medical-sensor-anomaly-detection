# tests/test_security.py
import pytest
from src.security import encryption  # Adjust import based on your actual implementation

def test_encryption():
    """Test the basic encryption functionality"""
    test_string = "test_data"
    encrypted = encryption.encrypt(test_string)
    
    assert encrypted != test_string
    decrypted = encryption.decrypt(encrypted)
    assert decrypted == test_string
