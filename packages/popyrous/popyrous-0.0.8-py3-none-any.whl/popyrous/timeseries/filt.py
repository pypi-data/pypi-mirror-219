
import numpy as np
from scipy.signal import butter, filtfilt, lfilter



# Designing lowpass filters
# Making different functions for smoothening (back-to-back filtering) and typical forward-filtering of timeseries data
def butter_lowpass_filter_back_to_back(data, cutoff, fs, order):
    """Low-pass filter the given data back-to-back (using filtfilt) using a Butterworth filter.

    ### Args:
        `data` (numpy array): Data, where each column is a timeseries, and each row is a time step.
        `cutoff` (float): Cutoff frequency, Hz
        `fs` (float): Sampling frequency, Hz
        `order` (int): Order of the filter

    ### Returns:
        Filtered Data
    """
    nyquist_freq = 0.5 * fs
    normal_cutoff = cutoff / nyquist_freq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    # print("a: ")
    # print(a)
    # print("b: ")
    # print(b)
    y = filtfilt(b, a, data.T).T
    # y = lfilter(b, a, data)
    return y




def butter_lowpass_filter_forward(data, cutoff, fs, order):
    """Low-pass filter the given data by only moving forwards (using filt, not filtfilt) using a Butterworth filter.

    ### Args:
        `data` (numpy array): Data, where each column is a timeseries, and each row is a time step.
        `cutoff` (float): Cutoff frequency, Hz
        `fs` (float): Sampling frequency, Hz
        `order` (int): Order of the filter

    ### Returns:
        Filtered Data
    """
    nyquist_freq = 0.5 * fs
    normal_cutoff = cutoff / nyquist_freq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    # y = filtfilt(b, a, data)
    y = lfilter(b, a, data.T).T
    
    return y