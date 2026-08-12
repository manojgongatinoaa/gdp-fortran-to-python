#!/usr/bin/python

# Here's a simple Python menu using the 'input()' function to run various commands:

# Programer: CG July 2026

from cridlist_according_drogue_status import according_drogue_status
from menu import Menu

def return_function(choice):
    if (abs(choice) == 5):
        according_drogue_status(choice)
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")       
    else:
        if (choice == 0):
            print('\n')
            print("Exit!")
    
def cridlist_main_menu():
    text = "M E N U (cridlist)"
    title = '\n' + f"{' ' * 9}{text}"  + '\n'
    title = title + f"{' ' * 9}{'=' * len(text)}"
    menu_dictionary = {
        "5. ": "All active buoys with drogue ON (-5 = with drogue OFF)" + '\n' + f"{' ' * 13}{'separated by manufacturer if needed'}"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, return_function)
    my_menu.loop()

if __name__ == "__main__":
    cridlist_main_menu()

