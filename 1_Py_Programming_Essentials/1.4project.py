""" Python Programming Essentials: Working with Dates Project Submission
Find a person's age in days
"""

import datetime

# Problem 1 Computing the number of days in a month
def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """
    date1 = datetime.date(year, month, 1)
    if month == 12:
        month = 0
        year += 1
    date2 = datetime.date(year, month + 1, 1)
    diff = date2 - date1
    return diff.days

# Problem 2 Checking if a date is valid
def is_valid_date(year, month, day):
    """
    Inputs:
      year  - an integer representing the year
      month - an integer representing the month
      day   - an integer representing the day

    Returns:
      True if year-month-day is a valid date and
      False otherwise
    """
    year_valid = datetime.MINYEAR <= year <= datetime.MAXYEAR
    if year_valid:
        month_valid = 1 <= month <= 12
        if month_valid:
            day_valid = 1 <= day <= days_in_month(year, month)
            if day_valid:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# Problem 3: Computing the number of days between two dates
def days_between(year1, month1, day1, year2, month2, day2):
    """
    Inputs:
      year1  - an integer representing the year of the first date
      month1 - an integer representing the month of the first date
      day1   - an integer representing the day of the first date
      year2  - an integer representing the year of the second date
      month2 - an integer representing the month of the second date
      day2   - an integer representing the day of the second date

    Returns:
      The number of days from the first date to the second date.
      Returns 0 if either date is invalid or the second date is
      before the first date.
    """
    if is_valid_date(year1, month1, day1) and is_valid_date(year2, month2, day2):
        date1 = datetime.date(year1, month1, day1)
        date2 = datetime.date(year2, month2, day2)
        if date1 < date2:
            diff = date2 - date1
            return diff.days
        else:
            return 0
    else:
        return 0

#Problem 4: Calculating a person's age in days
def age_in_days(year, month, day):
    """
    Inputs:
      year  - an integer representing the birthday year
      month - an integer representing the birthday month
      day   - an integer representing the birthday day

    Returns:
      The age of a person with the input birthday as of today.
      Returns 0 if the input date is invalid or if the input
      date is in the future.
    """
    if is_valid_date(year, month, day):
        today = datetime.date.today()
        day_age = days_between(year, month, day, today.year, today.month, today.day)
        return day_age
    else:
        return 0
