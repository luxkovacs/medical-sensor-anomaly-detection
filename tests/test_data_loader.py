# tests/test_data_loader.py
import pytest
import os
from pathlib import Path

def test_download_module_import():
    """Test if the download module can be imported"""
    from src.data import download
    assert download is not None
    assert hasattr(download, 'download_sleep_edf')

@pytest.mark.skip(reason="Downloads large files")
def test_download_sleep_edf_function():
    """Integration test for download function"""
    from src.data.download import download_sleep_edf
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        result_path = download_sleep_edf(target_dir=tmpdir)
        assert os.path.exists(result_path)
