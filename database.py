import sqlite3

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

    def __init__(self, username: str, db_name="finance_manager.db"):
        '''
        Initializes a new Person instance with a username and a zero balance.
        
        Args:
            username (str): The username of the person.
            db_name (str): The name of the database file.
        '''
        self.username = username
        self.expenses = {}  
        self.monthly_earnings = 0.0
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        '''
        Initializes the database and creates necessary tables.
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    monthly_earnings REAL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    username TEXT,
                    category TEXT,
                    amount REAL,
                    FOREIGN KEY(username) REFERENCES users(username)
                )
            ''')
            conn.commit()

    def register_user(self):
        '''
        Registers a new user and sets their monthly earnings.
        '''
        print(f"User {self.username} registered successfully.")
        while True:
            earnings_input = input("Enter your monthly earnings. This will be used to calculate your remaining balance: $")
            if earnings_input.replace('.', '', 1).isdigit() and earnings_input.count('.') <= 1:
                self.monthly_earnings = float(earnings_input)
                self._save_user_to_db()
                print(f"Monthly earnings set to: ${self.monthly_earnings:.2f}")
                break
            else:
                print("Invalid input. Please enter a valid number for your monthly earnings.")

    def _save_user_to_db(self):
        '''
        Saves the user's information to the database.
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (username, monthly_earnings)
                VALUES (?, ?)
            ''', (self.username, self.monthly_earnings))
            conn.commit()

    def display_information(self):
        '''
        Displays the current user's information such as their username, balance, and expenses.
        '''
        self._load_expenses_from_db()
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
            self._save_expense_to_db(category, amount)
            print(f"Added expense of ${amount:.2f} for {category}.")
        else:
            print("Invalid amount entered. Please enter a valid number for the expense.")

    def _save_expense_to_db(self, category, amount):
        '''
        Saves the expense to the database.
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (username, category, amount)
                VALUES (?, ?, ?)
            ''', (self.username, category, amount))
            conn.commit()
        self._load_expenses_from_db()

    def _load_expenses_from_db(self):
        '''
        Loads the user's expenses from the database.
        '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT category, SUM(amount) 
                FROM expenses
                WHERE username = ?
                GROUP BY category
            ''', (self.username,))
            self.expenses = {row[0]: row[1] for row in cursor.fetchall()}

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
