from scipy.optimize import curve_fit

## with some def voigt based on what you've already written

# def multi_voigt(x, sigma, gamma, amplitude, noise_std, nfit):
def multi_voigt(x, sigma, gamma, amplitude, noise_std, nfit):
    ## should work for nfit
    ## sigma, gamma, amplitude, noise will have to be lists


    for i in range(nfit):


def wrapper_fit_func(x, N, *args):
    a, b, c = list(args[0][:N]), list(args[0][N:2*N]), list(args[0][2*N:3*N])
    return fit_func(x, a, b, c, N)

def multi_voigt_wrapper()


def voigt_fit(voigt, wave, spec, nfit, **kwargs):

    popt, pcov = curve_fit(lambda x, sigma, gamma, amplitude, noise_std: multi_voigt(x, sigma, gamma, amplitude, noise_std, nfit), 
                           wave, spec, **kwargs)
    
    ## reorder popt to be sigma, gamma, amplitude, noise_std
    len_ = len(popt)/4
    sigma, gamma, amplitude, noise_std = popt[:len_], popt[len_:2*len_], popt[2*len_:3*len_], popt[3*len_:]
    
    return sigma, gamma, amplitude, noise_std