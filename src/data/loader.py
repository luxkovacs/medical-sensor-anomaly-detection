"""
Module for loading and processing EDF sleep data files.
"""
import os
import pandas as pd
import numpy as np
from pathlib import Path
import mne

class SleepEDFLoader:
    """
    Class for loading and processing Sleep-EDF data.
    """
    
    def __init__(self, data_dir=None):
        """
        Initialize the loader.
        
        Args:
            data_dir (str, optional): Directory with the Sleep-EDF data.
                                      Defaults to project's data/raw/sleep-edf directory.
        """
        if data_dir is None:
            # Determine the project root directory
            current_file_path = Path(__file__)
            project_root = current_file_path.parent.parent.parent
            self.data_dir = project_root / 'data' / 'raw' / 'sleep-edf'
        else:
            self.data_dir = Path(data_dir)
    
    def get_file_paths(self, limit=None):
        """
        Get paths to EDF files.
        
        Args:
            limit (int, optional): Limit the number of files returned. Defaults to None.
            
        Returns:
            list: List of tuples containing (PSG file path, Hypnogram file path)
        """
        psg_files = sorted([f for f in os.listdir(self.data_dir) if f.endswith('-PSG.edf')])
        hyp_files = sorted([f for f in os.listdir(self.data_dir) if f.endswith('-Hypnogram.edf')])
        
        if limit:
            psg_files = psg_files[:limit]
            hyp_files = hyp_files[:limit]
            
        return [(self.data_dir / psg, self.data_dir / hyp) for psg, hyp in zip(psg_files, hyp_files)]
    
    def load_edf_file(self, file_path):
        """
        Load an EDF file using MNE.
        
        Args:
            file_path (str): Path to the EDF file.
            
        Returns:
            mne.io.Raw: Loaded EDF data.
        """
        return mne.io.read_raw_edf(file_path, preload=True)
    
    def load_record(self, psg_path, hypnogram_path):
        """
        Load a complete sleep record (PSG data and hypnogram).
        
        Args:
            psg_path (str): Path to the PSG file.
            hypnogram_path (str): Path to the hypnogram file.
            
        Returns:
            tuple: (PSG data, hypnogram data)
        """
        psg_data = self.load_edf_file(psg_path)
        hypnogram = self.load_edf_file(hypnogram_path)
        
        return psg_data, hypnogram
    
    def extract_signals(self, raw_data, channels=None):
        """
        Extract signals from raw data.
        
        Args:
            raw_data (mne.io.Raw): Raw EDF data.
            channels (list, optional): List of channels to extract. 
                                       Defaults to EEG channels.
            
        Returns:
            pd.DataFrame: DataFrame with signals.
        """
        if channels is None:
            channels = [ch for ch in raw_data.ch_names if 'EEG' in ch]
        
        data, times = raw_data.get_data(return_times=True)
        data_dict = {ch: data[i] for i, ch in enumerate(raw_data.ch_names) if ch in channels}
        data_dict['time'] = times
        
        return pd.DataFrame(data_dict)

    def preprocess_eeg(self, eeg_data, lowcut=0.5, highcut=45, sampling_rate=100):
        """
        Apply basic preprocessing to EEG data.
        
        Args:
            eeg_data (pd.DataFrame): EEG data.
            lowcut (float): Low cut frequency for bandpass filter.
            highcut (float): High cut frequency for bandpass filter.
            sampling_rate (float): Sampling rate of the data.
            
        Returns:
            pd.DataFrame: Preprocessed EEG data.
        """
        # This is a placeholder for actual preprocessing
        # In a real implementation, you'd apply bandpass filtering, 
        # artifact removal, etc.
        return eeg_data
