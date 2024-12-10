import sqlite3

'''
This program tracks financial information from users' input and becomes stored within a table using sqlite 3

Driver/Navigator: Jayson Lee, Alejandra Saravia, Ester Manukyan
Assignment: Finance Manage Final Project
Date: 11/25/2024
'''

class Person:
    '''
    A class to represent a person who can register, track expenses, and view their financial information.
    '''
    
    def __init__(self, username: str, db_connection):
        '''
        Initializes a new Person instance with a username and database connection.
        
        Args:
            username (str): The username of the person.
            db_connection : connects to the SQLitedatabase
        '''

    
        self.username = username
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.expenses = {}
        self.monthly_earnings = 0.0

        # The "users" section of the table will be created  
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                monthly_earnings REAL
            )
        ''')
        # The "expenses" section of the table will be created  

        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS expenses (
                username TEXT,
                category TEXT,
                amount REAL,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        self.db_connection.commit()

    def register_user(self):
        '''
        A new user will be able to be created and their monthly earnings can be set.
        '''
        self.cursor.execute("SELECT username FROM users WHERE username = ?", (self.username,))
        if self.cursor.fetchone():
            print(f"Welcome back, {self.username}!")
            self.load_user_data()
        else:
            print(f"User {self.username} registered successfully.")
            while True:  
                earnings_input = input("Enter your monthly earnings. This will be used to calculate your remaining balance: $")
                if earnings_input.replace('.', '', 1).isdigit() and earnings_input.count('.') <= 1:
                    self.monthly_earnings = float(earnings_input)
                    self.cursor.execute("INSERT INTO users (username, monthly_earnings) VALUES (?, ?)", 
                                        (self.username, self.monthly_earnings))
                    self.db_connection.commit()
                    print(f"Monthly earnings set to: ${self.monthly_earnings:.2f}")
                    break
                else:
                    print("Invalid input. Please enter a valid number for your monthly earnings.")

    def load_user_data(self):
        '''
        Loads the user's data from the database, including monthly earnings and expenses.
        '''
        self.cursor.execute("SELECT monthly_earnings FROM users WHERE username = ?", (self.username,))
        self.monthly_earnings = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT category, amount FROM expenses WHERE username = ?", (self.username,))
        for category, amount in self.cursor.fetchall():
            self.expenses[category] = amount

    def display_information(self):
        '''
        Displays the current user's information: username, balance, and expenses.
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
        Asks the user for an expense amount and category. This amount will be added to the user's list of expenses.
        If the category already exists, it will update the existing category in the database.
        '''
        amount_input = input("\nEnter expense amount: $")
        if amount_input.replace('.', '', 1).isdigit() and amount_input.count('.') <= 1:
            amount = float(amount_input)
            category = input("Enter expense category (e.g., Food, Transportation, Rent, etc.): ").lower()

            if category in self.expenses:
                self.expenses[category] += amount
                self.cursor.execute("UPDATE expenses SET amount = ? WHERE username = ? AND category = ?", 
                                    (self.expenses[category], self.username, category))
            else:
                self.expenses[category] = amount
                self.cursor.execute("INSERT INTO expenses (username, category, amount) VALUES (?, ?, ?)", 
                                    (self.username, category, amount))
            self.db_connection.commit()
            print(f"Added expense of ${amount:.2f} for {category}.")
        else:
            print("Invalid amount entered. Please enter a valid number for the expense.")

    def calculate_balance(self):
        '''
        Calculates the user's remaining balance after subtracting all expenses from monthly earnings.
        
        Returns:
            float: The remaining account balance after expenses.
        '''
        total_expenses = sum(self.expenses.values())
        remaining_balance = self.monthly_earnings - total_expenses
        return remaining_balance

    def fetch_all_data(self):
        '''
        Fetches all rows from the users and expenses tables to display their contents.
        '''
        print("\n--- Users Table ---")
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for row in users:
            print(row)

        print("\n--- Expenses Table ---")
        self.cursor.execute("SELECT * FROM expenses")
        expenses = self.cursor.fetchall()
        for row in expenses:
            print(row)

def main():
    '''
    Main function that runs the financial tracking program.
    '''
    db_connection = sqlite3.connect("finance_manager.db")
    username = input("Enter your username: ")
    user = Person(username, db_connection)
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

    user.fetch_all_data()

    db_connection.close()

if __name__ == "__main__":
    main()
