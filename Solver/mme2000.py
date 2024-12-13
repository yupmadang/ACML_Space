import numpy as np

def mme2000(jdate):
    """
    Calculate the transformation matrix from EME2000 to the Mars mean equator and IAU node of epoch.

    Parameters:
        jdate (float): Julian date

    Returns:
        np.ndarray: Transformation matrix (3x3)
    """
    dtr = np.pi / 180.0
    t = (jdate - 2451545.0) / 36525.0

    # IAU 2000 pole orientation
    rasc_pole = 317.68143 - 0.1061 * t
    decl_pole = 52.88650 - 0.0609 * t

    phat_mars = np.zeros(3)
    phat_mars[0] = np.cos(rasc_pole * dtr) * np.cos(decl_pole * dtr)
    phat_mars[1] = np.sin(rasc_pole * dtr) * np.cos(decl_pole * dtr)
    phat_mars[2] = np.sin(decl_pole * dtr)

    # Unit pole vector in the J2000 system
    phat_j2000 = np.array([0.0, 0.0, 1.0])

    # IAU-defined x direction
    x_iau = np.cross(phat_j2000, phat_mars)
    x_iau = x_iau / np.linalg.norm(x_iau)

    # Y-direction
    yhat = np.cross(phat_mars, x_iau)
    yhat = yhat / np.linalg.norm(yhat)

    # Load elements of the transformation matrix
    tmatrix = np.zeros((3, 3))
    tmatrix[0, :] = x_iau
    tmatrix[1, :] = yhat
    tmatrix[2, :] = phat_mars

    return tmatrix
