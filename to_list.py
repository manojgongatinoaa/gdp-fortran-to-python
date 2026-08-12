#!/usr/bin/python

# Programer CG August 2026

# This .py file was created containing only a call to an external function
# to maintain consistency with the existing .for files.
# The name was changed from list.for to to_list.py because "list" is a reserved word in Python.

from inventory_menu import inventory_menu

# This function lists DIR-File records.
# Alternatively, it can create a file listing all buoys by experiment number
# or listing all buoys regardless of experiment number.
# Parameter:
#   jd_to_date     - Flag controlling date formatting. If True, timestamps convert 
#                    to Month/Day/Year. If False, they print as raw decimals.
def to_list(jd_to_date):
    # direp menu, option: 1. l i s t      buoys
    inventory_menu(jd_to_date)