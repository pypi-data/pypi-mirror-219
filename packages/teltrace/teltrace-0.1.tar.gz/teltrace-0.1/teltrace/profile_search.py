## still haven't found a database, so placeholder code in the meantime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_pressure(temp, species = 'h2o'):
    """
    Return pressure based on pressure-temperature curve for H2O or CO2.

    Parameters:
        temp (float): Temperature of planetary atmosphere in K.
        species (str): 'H2O' or 'CO2' -- species from which to calculate the pressure.
    
    Returns:
        pressure (float): Pressure in kPa.
    """
    if species.casefold() == 'h2o':

    if species.casefold() == 'co2':

    if species.caseefold() not in ['h2o', 'co2']:
        raise Exception('Specify chemical species -- "H2O" or "CO2"')

def object_profile(name, species = 'h2o',
                   figsize = (5, 5), color = 'gray', ls = '-', 
                   xlabel = 'x', ylabel = 'intensity', 
                   xscale = 'linear', yscale = 'linear'):
    """
    Return Voigt profile of line based on conditions of specific planet.

    Parameters:
        name (str): Name of planet (without spaces).
        species (str): 'H2O' or 'CO2' -- species from which to calculate the pressure.
            Passed to get_pressure().

        See matplotlib documentation for following --
            figsize (tuple): Size of plotted figure.
            color (str): Color of plotted profile.
            ls (str): Line style of plotted profile.
            xlabel (str): Label on x-axis of plotted figure.
            ylabel (str): Label on y-axis of plotted figure.
            xscale (str): Scaling of x-axis of plotted figure.
            yscale (str): Scaling of y-axis of plotted figure.
    
    Returns:
        Plot of line profile. 
    """

    props = pd.read_csv('PLACEHOLDER')

    if name.casefold() not in props.names.str.casefold():
        raise Exception('Planet conditions not found. List available planets with list_object.')
    
    if name.casefold() in props.names.str.casefold():
        planet_props = props.loc[props.names.str.casefold() == name.casefold()]

        press = get_pressure(planet_props.temp, species)

        x, spec = PLACEHOLDER_VOIGT_FUNCTION(planet_props.temp, press)

        fig = plt.figure(figsize = figsize)
        plt.plot(x, spec, color = color, ls = ls)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xscale(xscale)
        plt.yscale(yscale)

    

def list_object():
    props = pd.read_csv('PLACEHOLDER')
    for i in props.names.str.casefold():
        print(i)