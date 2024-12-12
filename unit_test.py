import unittest
import sqlite3
from io import StringIO
import sys
from unittest.mock import patch  

from database import Person

class TestPerson(unittest.TestCase):
    
    def setUp(self):
        """Set up the database connection and create the test"""
        self.db_name = "test_finance_manager.db"
        
        
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("DROP TABLE IF EXISTS expenses")
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error! {e}")

        self.db_connection = sqlite3.connect(self.db_name)
    
    def tearDown(self):
        """Close the database connection after each test."""
        self.db_connection.close()
    
    def test_register_user(self):
        """Test user registration and save to the database."""
        username = "testuser"
        person = Person(username, self.db_name)
        
        with patch('builtins.input', side_effect=["500"]):
            person.register_user()
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT username, monthly_earnings FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], username)
        self.assertEqual(result[1], 500.0)

    def test_add_expenses(self):
        """Test adding an expense and check if it's saved correctly."""
        username = "testuser"
        person = Person(username, self.db_name)  
        
        with patch('builtins.input', side_effect=["500"]):
            person.register_user()

        with patch('builtins.input', side_effect=["50", "food"]):
            person.want_add_expenses()
            
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT category, amount FROM expenses WHERE username = ?", (username,))
        result = cursor.fetchall()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "food")
        self.assertEqual(result[0][1], 50.0) 

    def test_calculate_balance(self):
        """Test balance calculation after adding expenses."""
        username = "testuser"
        person = Person(username, self.db_name)
        
        with patch('builtins.input', side_effect=["500"]):
            person.register_user()

        with patch('builtins.input', side_effect=["50", "food"]):
            person.want_add_expenses()

        balance = person.calculate_balance()
        self.assertEqual(balance, 450.0)  
    
    def test_display_information(self):
        """Test displaying the user's information (earnings, expenses, balance)."""
        username = "testuser"
        person = Person(username, self.db_name)
        
        with patch('builtins.input', side_effect=["500"]):
            person.register_user()

        with patch('builtins.input', side_effect=["50", "food"]):
            person.want_add_expenses()

        captured_output = StringIO()
        sys.stdout = captured_output
        
        person.display_information()

        self.assertIn("User: testuser", captured_output.getvalue())
        self.assertIn("Monthly Earnings: $500.00", captured_output.getvalue())
        self.assertIn("food: $50.00", captured_output.getvalue())
        self.assertIn("Remaining Balance: $450.00", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()