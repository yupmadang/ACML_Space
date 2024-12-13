def jd2str(jdate):
    """
    Convert Julian date to string equivalent of calendar date and universal time.

    Parameters:
        jdate (float): Julian date

    Returns:
        tuple:
            cdstr (str): Calendar date string
            utstr (str): Universal time string
    """
    from datetime import datetime, timedelta

    def gdate(jdate):
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

    # Get Gregorian date components
    month, day, year = gdate(jdate)

    # Create calendar date string
    calendar_date = datetime(year, month, int(day))
    cdstr = calendar_date.strftime("%m/%d/%Y")

    # Calculate fractional day to get the time
    fractional_day = day - int(day)
    time_of_day = timedelta(days=fractional_day)

    # Create universal time string
    base_time = datetime(year, month, int(day))
    ut_time = base_time + time_of_day
    utstr = ut_time.strftime("%H:%M:%S.%f")[:-3]  # Trim to milliseconds

    return cdstr, utstr
