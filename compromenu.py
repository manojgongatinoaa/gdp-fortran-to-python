#!/usr/bin/python

# Here's a simple Python menu using the 'input()' function to run various commands:
# Each option create a list of ids, reading the DIR-File (dirfl)

# Programer: CG July 2026

from cridlist import cridlist_main_menu
from helper import Menu

def return_function(choice):
    if (choice == 1):
        cridlist_main_menu()
    elif (choice == 2):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice == 3):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice == 4):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice == 5):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice == 6):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice == 7):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice == 8):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice == 9):
        print('\n' + f"{' ' * 9}{'*** To do ***'}")
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            print('\n')
            print("Goodbye!" + '\n')

def main_menu():
    title = '\n' + f"{' ' * 9}{'M E N U (comprocmenu)'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    menu_dictionary = {
        "1. ": "create list of ids (under construction - Ibis)",
        "2. ": "mainedit runstream",
        "3. ": "krignew runstream",
        "4. ": "work with wmogts file",
        "5. ": "create/update temp file (tmpfl.dat)",
        "6. ": "runstream to check for gaps (chktimdif3)",
        "7. ": "create a dire print out of sele ids",
        "8. ": "create runstream to run rdprint",
        "9. ": "update wmo# in direct file" + '\n' + f"{' ' * 13}{'from deployed.log, and find prog differences'}"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == "__main__":
    main_menu()

