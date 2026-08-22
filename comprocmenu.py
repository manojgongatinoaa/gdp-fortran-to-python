#!/usr/bin/python

# Here's a simple Python menu using the 'input()' function to run various commands:

# Programer: CG July 2026

from cridlist import cridlist_main_menu
from crtmpfl import crtmpfl30_main_menu
from crrunaccedit import crrunaccedit
from crrunkrig import crrunkrig
from menu import Menu

def return_function(choice):
    if (choice == 2):
        cridlist_main_menu()
    elif (choice == 3):
        crrunaccedit()
    elif (choice == 4):
        crrunkrig()
    elif (choice == 6):
        crtmpfl30_main_menu()
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            print('\n')
            print("Goodbye!" + '\n')

def main_menu():
    text = "M E N U (comprocmenu)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        " 2. ": "create list of ids",
        " 3. ": "create mainedit runstream",
        " 4. ": "create krignew runstream",
        " 5. ": "work with wmogts file",
        " 6. ": "create/update temp file (tmpfl30.dat)",
        " 7. ": "runstream to check for gaps (chktimdif3)",
        "10. ": "create a dire print out of sele ids",
        "14. ": "create runstream to run rdprint",
        "16. ": "update wmo# in direct file" + '\n' + f"{' ' * 14}{'from deployed.log, and find prog differences'}"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == "__main__":
    main_menu()

