import numpy as np

def kepler1(manom, ecc):
    """
    Solve Kepler's equation for circular, elliptic, and hyperbolic orbits using Danby's method.

    Parameters:
    manom : float
        Mean anomaly (radians).
    ecc : float
        Orbital eccentricity (non-dimensional).

    Returns:
    tuple
        eanom : float
            Eccentric anomaly (radians).
        tanom : float
            True anomaly (radians).
    """
    # Define convergence criterion
    ktol = 1.0e-10

    # Normalize mean anomaly to [0, 2*pi)
    xma = manom % (2 * np.pi)

    # Initial guess for eccentric anomaly
    if ecc == 0:
        # Circular orbit
        return xma, xma
    elif ecc < 1:
        # Elliptic orbit
        eanom = xma + 0.85 * np.sign(np.sin(xma)) * ecc
    else:
        # Hyperbolic orbit
        eanom = np.log(2 * xma / ecc + 1.8)

    # Perform iterations
    niter = 0
    while True:
        if ecc < 1:
            # Elliptic orbit
            s = ecc * np.sin(eanom)
            c = ecc * np.cos(eanom)

            f = eanom - s - xma
            fp = 1 - c
            fpp = s
            fppp = c
        else:
            # Hyperbolic orbit
            s = ecc * np.sinh(eanom)
            c = ecc * np.cosh(eanom)

            f = s - eanom - xma
            fp = c - 1
            fpp = s
            fppp = c

        niter += 1

        # Check for convergence
        if abs(f) <= ktol or niter > 20:
            break

        # Update eccentric anomaly using Danby's method
        delta = -f / fp
        deltastar = -f / (fp + 0.5 * delta * fpp)
        deltak = -f / (fp + 0.5 * deltastar * fpp + deltastar**2 * fppp / 6)

        eanom += deltak

    if niter > 20:
        raise RuntimeError("Kepler's equation did not converge after 20 iterations.")

    # Compute true anomaly
    if ecc < 1:
        # Elliptic orbit
        sta = np.sqrt(1 - ecc**2) * np.sin(eanom)
        cta = np.cos(eanom) - ecc
    else:
        # Hyperbolic orbit
        sta = np.sqrt(ecc**2 - 1) * np.sinh(eanom)
        cta = ecc - np.cosh(eanom)

    tanom = np.arctan2(sta, cta)

    return eanom, tanom
