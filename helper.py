#!/usr/bin/python

# programer: CG July 2026

# The Menu class is designed to handle user choices within a predefined dictionary of options.
# Each option is associated with a function that gets executed when the user selects it. 
# The menu offers the option to return to a specified function upon user request or exit the menu altogether.
class Menu:
    # Initialization: The Menu class is initialized with a dictionary of options 
    #                 and an optional return function. The dictionary holds the 
    #                 user choices, and the return function specifies where the 
    #                 user should be directed after interacting with the menu.
    def __init__(self, title, dictionary, last_option_description, return_function = None):
        self.title = title
        self.dictionary = dictionary
        # Adding the "Exit" option
        self.dictionary["0. "] = last_option_description # Adds a brand-new key-value pair
        self.return_function = return_function
        # Get the keys view
        # Convert every element to an integer
        self.all_options = [int(float(x)) for x in list(self.dictionary.keys())]
        self.last_option = str(self.all_options[-2])
    
    # Displaying Options: The display() method showcases the available options to 
    #                     the user, along with corresponding index numbers. The 
    #                     options are color-coded for improved visibility.        
    def display(self, index = 1):
        print(self.title)
        # Iterating through a dictionary
        # Loop through both keys and values simultaneously
        for key, value in self.dictionary.items():
            print(f"{' ' * 9}{key} {value}")

    # User Interaction Loop: The loop() method is the heart of the Menu class. 
    #                        It displays the menu, prompts the user for input, 
    #                        and executes the selected option's associated function.
    def loop(self):
        self.display()

        try:
            # The input() function always returns a string
            choice = int(input('\n' + f"{' ' * 9}{'Enter your choice (0-'}{self.last_option}{'): '}"))
            if (choice not in self.all_options):
                print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
                return self.loop()
            else :
                if callable(self.return_function(choice)):
                    self.return_function(choice)
                if (choice == 0):
                    pass
                else:
                    return self.loop()

        except ValueError as e:
            # Triggers if the user types letters, symbols, or floats instead of an integer
            print('\n' + f"{' ' * 9}{'Invalid input! Please enter a whole number.'}")
            return self.loop()

# Child class derived from Menu.
# This class keep looping while the user select a
# previous set choice.
class Loop_Menu(Menu):
    def __init__(self, title, dictionary, last_option_description, choice, return_function = None):
        # Call parent constructor to initialize the properties
        super().__init__(title, dictionary, last_option_description, return_function) 
        # Add a unique property for the child class
        self.choice = choice 

    # Overriding the parent's loop() method
    def loop(self):
        self.display()

        try:
            # The input() function always returns a string
            choice = int(input('\n' + f"{' ' * 9}{'Enter your choice (0-'}{self.last_option}{'): '}"))
            if (choice not in self.all_options):
                print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
                return self.loop()
            else :
                if callable(self.return_function(choice)):
                    self.return_function(choice)
                if (choice == 0 or choice == self.choice):
                    pass
                else:
                    return self.loop()

        except ValueError as e:
            # Triggers if the user types letters, symbols, or floats instead of an integer
            print('\n' + f"{' ' * 9}{'Invalid input! Please enter a whole number.'}")
            return self.loop()




