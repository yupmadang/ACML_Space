import numpy as np
from lambert import lambert  # Assuming glambert is implemented in a separate file
from p2000 import p2000

def pcfunc(jdate1, jdate2, mu, ip1, ip2, revmax):
    """
    Lambert delta-v function.

    Parameters:
        jdate1 (float): Departure Julian date.
        jdate2 (float): Arrival Julian date.
        mu (float): Gravitational constant of the central body.
        ip1 (int): ID of the departure body.
        ip2 (int): ID of the arrival body.
        revmax (int): Maximum number of revolutions.
        p2000 (function): Function to compute position and velocity state vectors.

    Returns:
        tuple: (dv1, dv2)
            dv1 (numpy array): Departure delta-v vector.
            dv2 (numpy array): Arrival delta-v vector.
    """
    # Time-of-flight in seconds
    taud = jdate2 - jdate1
    tof = taud * 86400.0

    # Compute initial state vector
    ri, vi = p2000(11, ip1, jdate1)

    # Compute final state vector
    rf, vf = p2000(11, ip2, jdate2)

    # Solve Lambert's problem
    sv1 = np.hstack((ri, vi))
    sv2 = np.hstack((rf, vf))

    vito, vfto = lambert(mu, sv1, sv2, tof, revmax)

    # Calculate departure delta-v vector
    dv1 = vito - vi

    # Calculate arrival delta-v vector
    dv2 = vf - vfto

    return dv1, dv2