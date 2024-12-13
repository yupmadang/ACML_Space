def juli(month, day, year):
    """
    Calculate the Julian date.

    Parameters:
        month (int): Calendar month [1 - 12].
        day (int): Calendar day [1 - 31].
        year (int): Calendar year [e.g., 2024].

    Returns:
        float: Julian date.

    Notes:
        - Handles pre-Gregorian calendar dates.
        - Reports invalid dates for October 5, 1582, to October 14, 1582.
    """
    y = year
    m = month
    b = 0
    c = 0

    if m <= 2:
        y -= 1
        m += 12

    if y < 0:
        c = -0.75

    # Check for valid calendar date
    if year < 1582:
        pass
    elif year > 1582:
        a = int(y / 100)
        b = 2 - a + (a // 4)
    elif month < 10:
        pass
    elif month > 10:
        a = int(y / 100)
        b = 2 - a + (a // 4)
    elif day <= 4:
        pass
    elif day > 14:
        a = int(y / 100)
        b = 2 - a + (a // 4)
    else:
        raise ValueError("This is an invalid calendar date!")

    jd = int(365.25 * y + c) + int(30.6001 * (m + 1))
    jdate = jd + day + b + 1720994.5

    return jdate 
"""
줄리안력으로 변환된 달력을 도출하여 활용함. 주로 천체 데이터를 활용하는 경우에 나타남.
변환된 일자를 pcfunc에 활용하니 오류가 생기면 변환 값을 찍어볼 것
"""
