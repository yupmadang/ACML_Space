def getdate():
    """
    Interactive request and input of calendar date.

    Returns:
        tuple: (month, day, year)
            month (int): Calendar month (1 <= month <= 12).
            day (int): Calendar day (1 <= day <= 31).
            year (int): Calendar year (all digits).
    """
    for attempt in range(5):
        print("\nPlease input the calendar date")
        print("(Format: month,day,year - 1 <= month <= 12, 1 <= day <= 31, year = all digits)")

        try:
            cdstr = input("? ").strip()
            
            # Split the input string by commas
            m, d, y = map(int, cdstr.split(","))

            # Validate inputs
            if 1 <= m <= 12 and 1 <= d <= 31:
                return m, d, y
            else:
                print("Invalid input. Please ensure the values are within valid ranges.")

        except (ValueError, IndexError):
            print("Invalid format. Please use the format: month,day,year")

    raise ValueError("Too many invalid attempts. Exiting.")