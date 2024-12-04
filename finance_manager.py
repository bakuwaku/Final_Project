'''
Tracks financial information from users' input.

Driver/Navigator: Jayson Lee, Alejandra Saravia, Ester Manukyan
Assignment: Finance Manage Final Project
Date: 11/25/2024
'''
class Person:
    '''
    A class to represent a person who can register, track expenses, 
    and view their financial information.
    '''
    
    def __init__(self, username: str):
        '''
        Initializes a new Person instance with a username and a zero balance.
        
        Args:
            username (str): The username of the person.
        '''
        self.username = username
        self.expenses = {}  
        self.monthly_earnings = 0.0

    def register_user(self):
        '''
        Registers a new user and sets their monthly earnings.
        '''
        print(f"User {self.username} registered successfully.")
        while True:  
            earnings_input = input("Enter your monthly earnings. This will be used to calculate your remaining balance: $")
            if earnings_input.replace('.', '', 1).isdigit() and earnings_input.count('.') <= 1:
                self.monthly_earnings = float(earnings_input)
                print(f"Monthly earnings set to: ${self.monthly_earnings:.2f}")
                break
            else:
                print("Invalid input. Please enter a valid number for your monthly earnings.")

    def display_information(self):
        '''
        Displays the current user's information such as their username, balance, and expenses.
        '''
        print(f"\nUser: {self.username}")
        print(f"Monthly Earnings: ${self.monthly_earnings:.2f}")
        print("Expenses (category):")
        for category, amount in self.expenses.items():
            print(f"{category}: ${amount:.2f}")
        remaining_balance = self.calculate_balance()
        print(f"Remaining Balance: ${remaining_balance:.2f}")

    def want_add_expenses(self):
        '''
        Asks the user for an expense amount and category, then adds it to the user's list of expenses.
        If the category already exists, it will add it to the existing category.
        '''
        amount_input = input("\nEnter expense amount: $")
        if amount_input.replace('.', '', 1).isdigit() and amount_input.count('.') <= 1:
            amount = float(amount_input)
            category = input("Enter expense category (e.g., Food, Transportation, Rent, etc.): ").lower()
            if category in self.expenses:
                self.expenses[category] += amount
            else:
                self.expenses[category] = amount
            print(f"Added expense of ${amount:.2f} for {category}.")
        else:
            print("Invalid amount entered. Please enter a valid number for the expense.")

    def calculate_balance(self):
        '''
        Calculates the user's remaining balance after subtracting the total expenses from monthly earnings.
        
        Returns:
            float: The remaining account balance after expenses.
        '''
        total_expenses = sum(self.expenses.values())
        remaining_balance = self.monthly_earnings - total_expenses
        return remaining_balance

def main():
    '''
    Main function to run the financial tracking program.
    '''
    username = input("Enter your username: ")
    user = Person(username)
    user.register_user()

    while True:
        ask_add_expense = input("\nDo you want to add an expense? (yes/no): ").lower()
        if ask_add_expense == 'yes':
            user.want_add_expenses()
        elif ask_add_expense == 'no':
            break
        else:
            print("Invalid input, please type 'yes' or 'no'.")

    user.display_information()

if __name__ == "__main__":
    main()

