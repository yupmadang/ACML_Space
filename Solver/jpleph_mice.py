import numpy as np
from spiceypy import furnsh, spkezr

# Global variables
iephem = 1
km = 1
au = 149597870.7  # Astronomical Unit in kilometers # Default ephemeris file

def initialize_ephemeris():
    """
    Initialize the SPICE ephemeris by loading the binary data file.
    """
    global iephem
    if iephem == 1:
        furnsh('D:\Yongjin\Code\ACML_Space\ACML_Space\data\de440.bsp')
        iephem = 0

def jpleph_mice(et, ntarg, ncent):
    """
    Reads the JPL planetary ephemeris and computes the position and velocity
    of the target point 'ntarg' relative to the center point 'ncent' using SPICE.

    Parameters:
    et : float
        TDB Julian date at which interpolation is wanted.
    ntarg : int
        Integer ID of the target point.
    ncent : int
        Integer ID of the center point.

        The numbering convention is:
        1 = Mercury, 2 = Venus, 3 = Earth, 4 = Mars,
        5 = Jupiter, 6 = Saturn, 7 = Uranus, 8 = Neptune,
        9 = Pluto, 10 = Moon, 11 = Sun.

    Returns:
    numpy.ndarray
        A 6-element array containing position and velocity of 'ntarg'
        relative to 'ncent'. Units are determined by the global variable 'km'.
    """
    initialize_ephemeris()

    # Define target and observer names
    bodies = {
        1: "mercury",
        2: "venus",
        3: "earth",
        4: "mars",
        5: "jupiter",
        6: "saturn",
        7: "uranus",
        8: "neptune",
        9: "pluto",
        10: "moon",
        11: "sun"
    }

    targ = bodies.get(ntarg, None)
    obs = bodies.get(ncent, None)

    if targ is None or obs is None:
        raise ValueError("Invalid target or center body ID.")

    # Compute ephemeris time in TDB seconds past J2000
    etime = 86400.0 * (et - 2451545.0)

    # Compute position and velocity vectors
    starg = spkezr(targ, etime, "J2000", "NONE", obs)

    # Provide output in user-requested units
    if km == 1:
        # Output in kilometers and kilometers/second
        rrd = starg[0]
    else:
        # Output in astronomical units and AU/day
        pos_au = starg[0][:3] / au
        vel_au_per_day = 86400.0 * starg[0][3:] / au
        rrd = np.concatenate((pos_au, vel_au_per_day))

    return np.array(rrd)
