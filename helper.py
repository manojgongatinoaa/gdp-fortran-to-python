# The Menu class is designed to handle user choices within a predefined dictionary of options.
# Each option is associated with a function that gets executed when the user selects it. 
# The menu offers the option to return to a specified function upon user request or exit the menu altogether.
class Menu:
    # Initialization: The Menu class is initialized with a dictionary of options 
    #                 and an optional return function. The dictionary holds the 
    #                 user choices, and the return function specifies where the 
    #                 user should be directed after interacting with the menu.
    def __init__(self, title, dictionary, last_option_description, option_function = None):
        self.title = title
        self.dictionary = dictionary
        # Adding the "Exit" option
        self.dictionary["0. "] = last_option_description # Adds a brand-new key-value pair
        self.option_function = option_function
    
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
            last_option = str(len(self.dictionary) - 1)
            choice = int(input('\n' + "          Enter your choice (0-" + last_option + "): "))
            if (abs(choice) < 0 or abs(choice) > int(last_option)):
                print('\n' + f"{' ' * 9}{'Invalid choice! Please try again.'}")
                return self.loop()
            else :
                if callable(self.option_function(choice)):
                    self.option_function(choice)
                if (choice == 0):
                    pass
                else:
                    return self.loop()

        except ValueError as e:
            # Triggers if the user types letters, symbols, or floats instead of an integer
            print('\n' + f"{' ' * 9}{'Invalid input! Please enter a whole number.'}")
            return self.loop()




