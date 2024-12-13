def gdate(jdate):
    """
    Convert Julian date to Gregorian (calendar) date.

    Parameters:
        jdate (float): Julian day

    Returns:
        tuple:
            month (int): Calendar month [1 - 12]
            day (float): Calendar day [1 - 31], may include fractional part
            year (int): Calendar year [yyyy]
    """
    jd = jdate

    z = int(jd + 0.5)
    fday = jd + 0.5 - z

    if fday < 0:
        fday += 1
        z -= 1

    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - int(alpha / 4)

    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e) + fday

    if e < 14:
        month = e - 1
    else:
        month = e - 13

    if month > 2:
        year = c - 4716
    else:
        year = c - 4715

    return month, day, year
