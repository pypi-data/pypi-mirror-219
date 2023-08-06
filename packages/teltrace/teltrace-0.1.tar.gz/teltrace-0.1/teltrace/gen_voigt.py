import numpy as np
from scipy.special import wofz
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.constants as c

def voigt(x, dx, sigma, gamma, amplitude):
    """Generate a Voigt profile at positions x, given the parameters sigma and gamma.

    Args: 
        x (arr): given to generate the Voigt profile
        dx (float): location of the center of the profile
        sigma(float): parameter characterizing the Voigt profile
        gamma(float): parameter characterizing the Voigt profile
        amplitude(float): amplitude of the Voigt profile
    Returns:
        v (arr): y values of the Voigt profile
        
    """
    z = ((x-dx) + 1j*gamma) / (sigma * np.sqrt(2))
    v = amplitude*np.real(wofz(z)) / (sigma * np.sqrt(2*np.pi))
    return v

def generate_voigt_profile(x,dx, sigma, gamma, amplitude, noise_std=0):
    """Generate a Voigt profile with given parameters at positions x, including Gaussian noise.
    
    Args: 
        x (arr): given to generate the Voigt profile
        dx (float): location of the center of the profile
        sigma(float): parameter characterizing the Voigt profile
        gamma(float): parameter characterizing the Voigt profile
        amplitude(float): amplitude of the Voigt profile
        noise_std(float): standard deviation of noise to be applied to Voigt profile
                        default is 0
    
    Returns:
        y_with_noise (arr): Voigt profile with Gaussian noise

    """
    y = voigt(x, dx, sigma, gamma, amplitude)
    noise = np.random.normal(0, noise_std, len(x))
    y_with_noise = y + noise
    return y_with_noise

#Example
#------------------------------
# Generate x values
x = np.linspace(-10, 10, 1000)
dx = 0
# Set initial parameter values
sigma = 1.0
gamma = 1.0
amplitude = 100.0
noise_std = 0.1  # Standard deviation of the Gaussian noise

# Generate Voigt profile with noise
y = generate_voigt_profile(x,dx, sigma, gamma, amplitude, noise_std)

# Plot the Voigt profile with noise
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('Intensity')
plt.title('Voigt Profile with Noise')
plt.show()

#Saving to a .csv file
# data = np.column_stack((x, y))
# np.savetxt('voigt_data.csv', data, delimiter=',', header='x,y', fmt='%.6f', comments='')



### from https://academic.oup.com/mnras/article/458/2/1427/2589008
def gamma_g(temp, species, v0):
    """
    Return the width of the Gaussian component of the Voigt profile.

    Parameters:
        temp (float): Temperature of planetary atmosphere in K.
        species (str): 'H2O' or 'CO2' -- species from which to calculate the pressure.
        v0 (float): Central wavenumber of line -- in 1/cm.

    Returns:
        gamma_g (float): Width of Gaussian component of Voigt profile in 1/cm.
    """
    if species.casefold() == 'h2o':
        mass = (2*c.m_p +  8*c.m_p).to(u.g)
    if species.casefold() == 'co2':
        mass = (6*c.m_p + 16*c.m_p).to(u.g)

    if species.caseefold() not in ['h2o', 'co2']:
        raise Exception('Specify chemical species -- "H2O" or "CO2"')
    
    gamma_g = np.sqrt(2*c.k_B*temp*u.K/mass) * (v0/u.cm)/c.c.to(u.cm/u.s)).to(1/u.cm)

    return gamma_g.value

def gamma_l(temp, press, species):
    """
    Return the width of the Lorentzian component of the Voigt profile.

    Parameters:
        temp (float): Temperature of planetary atmosphere in K.
        press (float): Pressure in kPa.
        species (str): 'H2O' or 'CO2' -- species from which to calculate the pressure.

    Returns:
        gamma_l (float): Width of Lorentzian component of Voigt profile in 1/cm.
    """
    if species.casefold() == 'h2o':
        n = 0.58 ## mean for broadening due to air across H_2^16O transitions from HITRAN
        gl_mol = 0.068 ## mean for broadening due to air across H_2^16O transitions from HITRAN
    if species.casefold() == 'co2':
        n = 0.71 ## mean for broadening due to air across ^12C^16O_2 transitions from HITRAN
        gl_mol = 0.070 ## mean for broadening due to air across ^12C^16O_2 transitions from HITRAN
    if species.caseefold() not in ['h2o', 'co2']:
        raise Exception('Specify chemical species -- "H2O" or "CO2"')

    partial_press = 1 #partial pressure, assuming only one species and isotopologue, so = 1

    gamma_l = ((temp*u.K)/(296*u.K))**n * press*u.kPa.to(u.atm) * (gl_mol/(u.cm*u.atm) * partial_press) #would sum, but only one species

    return gamma_l.to(1/u.cm).value

def gamma_voigt(temp, press, species, v0):
    """
    Return the Voigt profile width based on Gaussian and Lorentzian components.

    Parameters:
        temp (float): Temperature of planetary atmosphere in K.
        press (float): Pressure in kPa.
        species (str): 'H2O' or 'CO2' -- species from which to calculate the pressure.
        v0 (float): Central wavenumber of line -- in 1/cm.
    
    Returns:
        gamma_voigt (float): Width of Voigt profile in 1/cm.
    """
    gg = gamma_g()
    gl = gamma_l()

    return 0.5346*gl + np.sqrt(0.2166*gl**2 + gg**2)