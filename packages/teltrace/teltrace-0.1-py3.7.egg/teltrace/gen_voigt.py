import numpy as np
from scipy.special import wofz
import matplotlib.pyplot as plt

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