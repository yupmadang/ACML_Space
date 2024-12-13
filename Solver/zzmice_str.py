def zzmice_str(x, empty=False):
    """
    Ensures the input is a string or a list of strings. Converts a list of strings to a single string.

    Parameters:
    x (str or list of str): Input to validate and convert.
    empty (bool): Whether to allow empty strings. Defaults to False.

    Returns:
    str: The validated and converted string.

    Raises:
    ValueError: If input is not a string or list of strings, or if empty strings are not allowed.
    """
    # Check the type of `x`
    if isinstance(x, list):
        # Convert list of strings to a single string
        if all(isinstance(item, str) for item in x):
            x = ''.join(x)
        else:
            raise ValueError("Input must be a list of strings or a single string.")

    if isinstance(x, str):
        # Input is already a string
        y = x
    else:
        # Input is neither a string nor a list of strings
        raise ValueError("Input must be a string or a list of strings.")

    # Check for empty string if not allowed
    if not empty and len(y) == 0:
        raise ValueError("Empty strings are not allowed.")

    return y
