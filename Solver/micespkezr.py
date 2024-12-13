import spiceypy as spice

def mice_spkezr(targ, et, ref, abcorr, obs):
    """
    Get the state (position and velocity) of a target body relative to an observer.

    Parameters:
    targ (str): Name or ID of the target body.
    et (float or list of float): Ephemeris time(s) in seconds past J2000 TDB.
    ref (str): Reference frame (e.g., 'J2000').
    abcorr (str): Aberration correction flag (e.g., 'LT+S').
    obs (str): Name or ID of the observer body.

    Returns:
    dict: A dictionary containing the state vector and light time:
        - 'state': [x, y, z, vx, vy, vz] (position in km, velocity in km/s)
        - 'lt': Light time in seconds
    """
    try:
        # Validate inputs
        targ = str(targ)
        et = float(et) if isinstance(et, (int, float)) else list(map(float, et))
        ref = str(ref)
        abcorr = str(abcorr)
        obs = str(obs)

        # Call SPICE function
        state, lt = spice.spkezr(targ, et, ref, abcorr, obs)

        return {
            'state': state.tolist(),
            'lt': lt
        }

    except spice.support_types.SpiceyError as e:
        raise ValueError(f"SPICE error: {str(e)}")