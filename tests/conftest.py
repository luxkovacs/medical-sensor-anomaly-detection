import pytest
from src.security import encryption  # Adjust import based on your actual implementation

@pytest.fixture
def sample_fixture():
    return "sample data"

def test_encryption():
    """Test the basic encryption functionality"""
    test_string = "test_data"
    encrypted = encryption.encrypt(test_string)
    
    assert encrypted != test_string
    decrypted = encryption.decrypt(encrypted)
    assert decrypted == test_string
