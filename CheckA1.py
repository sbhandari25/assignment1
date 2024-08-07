#!/usr/bin/env python3

import unittest
from datetime import datetime, date, timedelta
from random import randint, shuffle
import sys, os
import subprocess as sp
from importlib import import_module

'''
ASSIGNMENT 1 CHECK SCRIPT
Summer 2023
Author: Eric Brauer eric.brauer@senecacollege.ca

Description:
TestAfter .. TestDBDA all are testing functions inside students' code. 
TestFinal will run the code as a subprocess and evaluate the std.output.

The precise requirements of each student-created function are specified elsewhere.

The script assumes that the student's filename is named 'assignment1.py' and exists in the same directory as this check script.

NOTE: Feel free to _fork_ and modify this script to suit needs. I will try to fix any issues that arise but this script is provided as-is, with no obligation of warranty or support.
'''

class TestAfter(unittest.TestCase):

    def setUp(self):
        self.filename = 'assignment1.py'
        self.pypath = sys.executable
        error_output = f'{self.filename} cannot be found (HINT: make sure this script AND your file are in the same directory)'
        file = os.path.join(os.getcwd(), self.filename)
        self.assertTrue(os.path.exists(file), msg=error_output)
        try:
            self.a1 = import_module(self.filename.split('.')[0])
        except ModuleNotFoundError:
            print("Cannot find a function inside your assignment1.py. Do not rename or delete any of the required functions.")

    def test_dtypes(self):
        "after() is returning string"
        i = '01/10/2023'
        error_msg = 'Your after() function should accept one string as arg, and return a string.'
        self.assertIsInstance(self.a1.after(i), str, error_msg)
    
    def rando_date_str(self):
        invalid = True
        while invalid:
            y = randint(1800, 2100)
            m = randint(1, 12)
            d = randint(1, 31)
            try:
                x = date(y, m, d)
                x.strftime('%d/%m/%Y')
                invalid = False
            except ValueError:
                pass
        return x.strftime('%d/%m/%Y')

    def test_after_date(self):
        "after() works"
        error_msg = "Running after() with date arg should return the next day"
        for _ in range(20):
            datestr = self.rando_date_str()
            dt = datetime.strptime(datestr, '%d/%m/%Y')
            next_day = dt + timedelta(days=1)
            e = next_day.strftime('%d/%m/%Y')
            self.assertEqual(self.a1.after(datestr), e, error_msg)
    
    def test_leap(self):
        "after() works with leap year"
        date1 = "28/02/2020"
        e = "29/02/2020"
        error_msg = f"Running after({date1})"
        self.assertEqual(self.a1.after(date1), e, error_msg)

class TestLeap(unittest.TestCase):
    def setUp(self):
        self.a1 = import_module('assignment1')

    def test_leap_func(self):
        error_msg = "leap_year function exists and returns True/False"
        for i, e in [(1600, True), (2020, True), (2100, False), (1900, False), (2000, True), (2019, False)]:
            self.assertEqual(self.a1.leap_year(i), e, error_msg)

class TestMonMax(unittest.TestCase):
    def setUp(self):
        self.a1 = import_module('assignment1')

    def test_leap_max(self):
        error_msg = "test mon_max with feb of leap/non-leap years"
        for i, j, e in [(2020, 2, 29), (2021, 2, 28)]:
            self.assertEqual(self.a1.mon_max(j, i), e, error_msg)

    def test_mon_max(self):
        error_msg = "test the mon_max function"
        for i, j, e in [(2021, 1, 31), (2021, 3, 31), (2021, 4, 30), (2021, 6, 30)]:
            self.assertEqual(self.a1.mon_max(j, i), e, error_msg)

class TestValidDate(unittest.TestCase):
    def setUp(self):
        self.a1 = import_module('assignment1')

    def test_valid_dates(self):
        error_msg = "making sure valid dates return True"
        for i in ["2021-01-01", "2020-02-29", "2019-12-31"]:
            self.assertTrue(self.a1.valid_date(i), error_msg)

    def test_invalid_dates(self):
        error_msg = "making sure invalid dates return False"
        for i in ["2021-02-29", "2020-04-31", "2019-13-01"]:
            self.assertFalse(self.a1.valid_date(i), error_msg)

class TestDayCount(unittest.TestCase):
    def setUp(self):
        self.a1 = import_module('assignment1')

    def test_day_count(self):
        error_msg = "day_count should return the correct number of days between two dates"
        for start, end, count in [("2021-01-01", "2021-01-10", 10), ("2020-02-28", "2020-03-01", 3), ("2020-01-01", "2020-01-01", 1)]:
            self.assertEqual(self.a1.day_count(start, end), count, error_msg)

class TestFinal(unittest.TestCase):
    def setUp(self):
        self.a1 = import_module('assignment1')
    
    def test_arg_length(self):
        with self.assertRaises(SystemExit):
            self.a1.print_usage()

    def test_invalid_date(self):
        with self.assertRaises(SystemExit):
            self.a1.print_usage()

    def test_invalid_num(self):
        with self.assertRaises(SystemExit):
            self.a1.print_usage()

    def test_neg_arg(self):
        start_date = "13/08/1881"
        num_days = -208
        e = "The end date is Mon, 17/01/1881."
        output = self.a1.day_iter(start_date, num_days)
        error_msg = f'Running your script with arguments "{start_date} {num_days}" should return the output:"{e}"'
        self.assertIn(e, output, error_msg)

if __name__ == "__main__":
    unittest.main(buffer=True)  # buffer line suppresses a1 printlines from check script output.

