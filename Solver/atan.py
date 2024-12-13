import numpy as np

def atan3(a, b):
    """
    Four-quadrant inverse tangent function.

    Parameters:
        a (float): Sine of the angle
        b (float): Cosine of the angle

    Returns:
        float: Angle in radians (0 <= y < 2 * pi)
    """
    epsilon = 1e-10
    pidiv2 = 0.5 * np.pi

    if abs(a) < epsilon:
        return (1 - np.sign(b)) * pidiv2

    c = (2 - np.sign(a)) * pidiv2

    if abs(b) < epsilon:
        return c

    return c + np.sign(a) * np.sign(b) * (abs(np.arctan(a / b)) - pidiv2)