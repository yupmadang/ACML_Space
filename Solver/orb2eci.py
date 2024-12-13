import numpy as np

def orb2eci(mu, oev):
    """
    Convert classical orbital elements to ECI state vector.

    Parameters:
    mu : float
        Gravitational constant (km^3/s^2)
    oev : list or numpy.ndarray
        Orbital elements:
        oev[0] = semimajor axis (km)
        oev[1] = orbital eccentricity (0 <= ecc < 1)
        oev[2] = orbital inclination (radians, 0 <= inc <= pi)
        oev[3] = argument of perigee (radians, 0 <= argper <= 2*pi)
        oev[4] = right ascension of ascending node (radians, 0 <= raan <= 2*pi)
        oev[5] = true anomaly (radians, 0 <= tanom <= 2*pi)

    Returns:
    tuple
        r : numpy.ndarray
            ECI position vector (km)
        v : numpy.ndarray
            ECI velocity vector (km/s)
    """
    # Initialize position and velocity vectors
    r = np.zeros(3)
    v = np.zeros(3)

    # Unpack orbital elements
    sma, ecc, inc, argper, raan, tanom = oev

    # Semi-latus rectum
    slr = sma * (1 - ecc**2)

    # Radius magnitude
    rm = slr / (1 + ecc * np.cos(tanom))

    # Argument of latitude
    arglat = argper + tanom

    # Precompute trigonometric functions
    sarglat = np.sin(arglat)
    carglat = np.cos(arglat)

    c4 = np.sqrt(mu / slr)
    c5 = ecc * np.cos(argper) + carglat
    c6 = ecc * np.sin(argper) + sarglat

    sinc = np.sin(inc)
    cinc = np.cos(inc)

    sraan = np.sin(raan)
    craan = np.cos(raan)

    # Compute position vector
    r[0] = rm * (craan * carglat - sraan * cinc * sarglat)
    r[1] = rm * (sraan * carglat + cinc * sarglat * craan)
    r[2] = rm * sinc * sarglat

    # Compute velocity vector
    v[0] = -c4 * (craan * c6 + sraan * cinc * c5)
    v[1] = -c4 * (sraan * c6 - craan * cinc * c5)
    v[2] = c4 * c5 * sinc

    return r, v