# This was derived from stack overflow
# https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units

import numpy as np
from scipy.signal import butter, lfilter, freqz
from scipy.io import wavfile
import matplotlib.pyplot as plt


def _butter(cutoff, fs, btype, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return b, a


def filterData(data, cutoff, fs, btype, order=5):
    b, a = _butter(cutoff, fs, btype, order=order)
    y = lfilter(b, a, data)
    return y


def filterFile(inputFn, outputFn, cutoff, btype, order=5):
    """
    Highpass or lowpass a file

    Highpass -- frequencies above the cutoff are kept, others removed
    Lowpass -- frequenices below the cutoff are kept, others removed

    cutoff - integer: the cutoff frequency
    btype - string: one of 'lowpass' or 'highpass'
    order - the order of the filter
    """
    assert btype in ["lowpass", "highpass"]
    fs, data = wavfile.read(inputFn)
    filteredData = filterData(data, cutoff, fs, btype, order)
    wavfile.write(outputFn, fs, filteredData)
