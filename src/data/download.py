"""
Module for downloading and extracting the Sleep-EDF Database Expanded.
"""
import os
import subprocess
import sys
import zipfile
from pathlib import Path

def download_sleep_edf(target_dir=None, version='1.0.0'):
    """
    Download the Sleep-EDF Database Expanded from PhysioNet.
    
    Args:
        target_dir (str, optional): Directory to save the dataset. 
                                    Defaults to project's data/raw directory.
        version (str, optional): Version of the dataset. Defaults to '1.0.0'.
    
    Returns:
        Path: Path to the downloaded dataset directory
    """
    # Define URLs and paths
    physionet_url = f"https://physionet.org/content/sleep-edfx/{version}/"
    
    if target_dir is None:
        # Determine the project root directory
        current_file_path = Path(__file__)
        project_root = current_file_path.parent.parent.parent
        target_dir = project_root / 'data' / 'raw'
    else:
        target_dir = Path(target_dir)
        
    # Create target directory if it doesn't exist
    extract_dir = target_dir / "sleep-edf"
    os.makedirs(extract_dir, exist_ok=True)
    
    # Use wget to download files (works on Windows with appropriate installation)
    try:
        print(f"Downloading Sleep-EDF data to {extract_dir}...")
        print("This might take a while (dataset is 8.1 GB)...")
        
        # Check if wget is available 
        subprocess.run(["wget", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Download using wget
        cmd = ["wget", "-r", "-N", "-c", "-np", 
               "--directory-prefix", str(extract_dir),
               f"{physionet_url}"]
        
        subprocess.run(cmd, check=True)
        print(f"Download complete. Data saved to {extract_dir}")
    except Exception as e:
        print(f"Error using wget: {e}")
        print("\nManual download instructions:")
        print(f"1. Visit {physionet_url}")
        print("2. Download the ZIP file (8.1 GB)")
        print("3. Extract the ZIP to:", extract_dir)
        print("\nAlternatively, use one of these commands in a terminal:")
        print(f"wget -r -N -c -np --directory-prefix={extract_dir} {physionet_url}")
        print("\nOr using AWS CLI:")
        print(f"aws s3 sync --no-sign-request s3://physionet-open/sleep-edfx/{version}/ {extract_dir}")
        
    return extract_dir

if __name__ == "__main__":
    download_sleep_edf()
