
def t_lorentzian(t, u, fwhm, A=1, phi=0):
    """
    Lorentzian function in the time domain.
    --------
    Parameters
    - t: 1darray
        Independent variable
    - u: float
        Peak position
    - fwhm: float
        Full-width at half-maximum, 2γ
    - A: float
        Intensity
    - phi: float
        Phase, in radians
    --------
    Returns
    - S: 1darray
        Lorentzian function.
    """
    hwhm = np.abs(fwhm) / 2       
    S = A * np.exp(1j*phi) * np.exp((1j *2*np.pi *u * t)-(t*hwhm))
    return S
