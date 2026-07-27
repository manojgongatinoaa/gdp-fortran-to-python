# Here's a simple Python menu using the 'input()' function to run various commands:
# Each option create a list of ids, reading the DIR-File (dirfl)

#Programer: CG July 2026

from cridlist import cridlist_main_menu
from helper import Menu

def option_2():
    print("You selected Option 2.")
    # Add your command logic here for Option 2

def option_3():
    print("You selected Option 3.")
    # Add your command logic here for Option 3

def option_4():
    print("You selected Option 4.")
    # Add your command logic here for Option 4

def option_5():
    print("You selected Option 5.")
    # Add your command logic here for Option 5

def option_6():
    print("You selected Option 6.")
    # Add your command logic here for Option 6

def option_7():
    print("You selected Option 7.")
    # Add your command logic here for Option 7

def option_8():
    print("You selected Option 8.")
    # Add your command logic here for Option 8

def option_9():
    print("You selected Option 9.")
    # Add your command logic here for Option 9

def option_function(choice):
    if (choice == 1):
        cridlist_main_menu()
    elif (choice < 0):
        print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
    else:
        if (choice == 0):
            print('\n' + f"{' ' * 9}{'Goodbye!'}" + '\n')

def main_menu():
    title = '\n' + f"{' ' * 9}{'M E N U (comprocmenu)'}"  + '\n'
    title = title + f"{' ' * 9}{'=========================='}"
    menu_dictionary = {
        "1. ": "create list of ids (UNDER CONSTRUCTION)",
        "2. ": "mainedit runstream (TO DO)",
        "3. ": "krignew runstream (TO DO)",
        "4. ": "work with wmogts file (TO DO)",
        "5. ": "create/update temp file (tmpfl.dat) (TO DO)",
        "6. ": "runstream to check for gaps (chktimdif3) (TODO)",
        "7. ": "create a dire print out of sele ids (TO DO)",
        "8. ": "create runstream to run rdprint (TO DO)",
        "9. ": "update wmo# in direct file (TO DO)" + '\n' + f"{' ' * 13}{'from deployed.log, and find prog differences'}"
    }
    last_option_description = "Exit"

    my_menu = Menu(title, menu_dictionary, last_option_description, option_function)
    my_menu.loop()

if __name__ == "__main__":
    main_menu()

