def zzmice_dp(x, nanok=False):
    """
    Converts a numeric input to double precision and checks for NaN values.

    Parameters:
    x (numeric): Input numeric to convert to double precision.
    nanok (bool): Whether NaN values are allowed. Defaults to False.

    Returns:
    numpy.ndarray or float: The double precision representation of `x`.

    Raises:
    ValueError: If input is not numeric or contains NaN values when `nanok` is False.
    """
    import numpy as np

    # Check if the input is numeric
    if not (isinstance(x, (int, float, np.ndarray)) or np.isscalar(x)):
        raise ValueError("Input must be numeric, such as an integer, float, or a numeric array.")

    # Convert input to a numpy array for consistent handling
    x = np.asarray(x, dtype=np.float64)

    # Check for NaN values if not allowed
    if not nanok and not np.all(np.isfinite(x)):
        raise ValueError("Input contains NaN or infinite values, which are not allowed.")

    # Convert input to double precision
    return x