import numpy as np
import pandas as pd
import astropy.io.fits as fits


def file_read(filepath):
    """Read a .csv file into a dataframe to be manipulated

    Args:
        filepath: (str, path object, or file-like object) .csv file to be read in

    Returns:
        spectrum (pandas.df) Dataframe containing wavenumber information
        in the first column and intensity of line information in the second column
    """
    #load a .csv file and output a dataframe with wavelength and intensity information
    spectrum  = pd.read_csv(filepath, header=[0])
    #rename columns
    spectrum.columns.values[0] = 'Wavenumber'
    spectrum.columns.values[1] = 'Intensity'
    return spectrum

