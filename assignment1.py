#!/usr/bin/env python3

'''
OPS445 Assignment 1 - Fall 2023
Program: assignment1.py 
The python code in this file is original work written by
"Santosh Bhandari". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Author: Santosh Bhandari
Description: Calculates number of weekend days between two dates
'''

import sys

def day_of_week(date: str) -> str:
    "Based on the algorithm by Tomohiko Sakamoto"
    day, month, year = (int(x) for x in date.split('/'))
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    offset = {1: 0, 2: 3, 3: 2, 4: 5, 5: 0, 6: 3, 7: 5, 8: 1, 9: 4, 10: 6, 11: 2, 12: 4}
    if month < 3:
        year -= 1
    num = (year + year // 4 - year // 100 + year // 400 + offset[month] + day) % 7
    return days[num]

def leap_year(year: int) -> bool:
    "Return true if the year is a leap year"
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def mon_max(month: int, year: int) -> int:
    "Returns the maximum day for a given month. Includes leap year check"
    if month == 2 and leap_year(year):
        return 29
    else:
        return {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}[month]

def after(date: str) -> str:
    '''
    after() -> date for next day in DD/MM/YYYY string format

    Return the date for the next day of the given date in DD/MM/YYYY format.
    This function has been tested to work for year after 1582
    '''
    day, mon, year = (int(x) for x in date.split('/'))
    day += 1  # next day

    if day > mon_max(mon, year):
        mon += 1
        if mon > 12:
            year += 1
            mon = 1
        day = 1  # if tmp_day > this month's max, reset to 1
    return f"{day:02}/{mon:02}/{year}"

def before(date: str) -> str:
    '''
    before() -> date for the previous day in DD/MM/YYYY string format

    Return the date for the previous day of the given date in DD/MM/YYYY format.
    This function has been tested to work for year after 1582
    '''
    day, mon, year = (int(x) for x in date.split('/'))
    day -= 1  # previous day

    if day < 1:
        mon -= 1
        if mon < 1:
            year -= 1
            mon = 12
        day = mon_max(mon, year)  # set to previous month's max

    return f"{day:02}/{mon:02}/{year}"

def print_usage():
    "Print a usage message to the user"
    print("Usage: " + str(sys.argv[0]) + " YYYY-MM-DD NN")
    sys.exit()

def valid_date(date: str) -> bool:
    "Check validity of date"
    try:
        year, month, day = (int(x) for x in date.split('-'))
        return 1 <= month <= 12 and 1 <= day <= mon_max(month, year)
    except ValueError:
        return False

def day_iter(start_date: str, num: int) -> str:
    "Iterates from start date by num to return end date in YYYY-MM-DD"
    start_date_ddmmyyyy = convert_to_ddmmyyyy(start_date)
    for _ in range(abs(num)):
        if num > 0:
            start_date_ddmmyyyy = after(start_date_ddmmyyyy)
        else:
            start_date_ddmmyyyy = before(start_date_ddmmyyyy)
    return convert_to_yyyymmdd(start_date_ddmmyyyy)

def day_count(start_date: str, end_date: str) -> int:
    "Returns the number of days between start_date and end_date, inclusive"
    start_date_ddmmyyyy = convert_to_ddmmyyyy(start_date)
    end_date_ddmmyyyy = convert_to_ddmmyyyy(end_date)
    count = 0
    while start_date_ddmmyyyy != end_date_ddmmyyyy:
        start_date_ddmmyyyy = after(start_date_ddmmyyyy)
        count += 1
    return count + 1  # Include the end_date itself

def convert_to_ddmmyyyy(date: str) -> str:
    "Converts a date from YYYY-MM-DD to DD/MM/YYYY format"
    if '-' in date:
        year, month, day = date.split('-')
        return f"{day}/{month}/{year}"
    return date

def convert_to_yyyymmdd(date: str) -> str:
    "Converts a date from DD/MM/YYYY to YYYY-MM-DD format"
    if '/' in date:
        day, month, year = date.split('/')
        return f"{year}-{month}-{day}"
    return date

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()

    start_date = sys.argv[1]
    num_days = sys.argv[2]

    if not valid_date(start_date):
        print_usage()

    try:
        num_days = int(num_days)
    except ValueError:
        print_usage()

    end_date = day_iter(start_date, num_days)
    end_date_ddmmyyyy = convert_to_ddmmyyyy(end_date)
    end_date_day_of_week = day_of_week(end_date_ddmmyyyy)

    print(f'The end date is {end_date_day_of_week}, {end_date_ddmmyyyy}.')

