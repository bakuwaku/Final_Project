import unittest
from unittest.mock import patch
from io import StringIO
from finance_manager import Person 

class TestPerson(unittest.TestCase):
    def setUp(self):
        """Set up a sample person for testing."""
        self.user = Person("test_user")
    
    @patch('builtins.input', side_effect=["5000"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_register_user(self, mock_stdout, mock_input):
        """Test user registration and setting monthly earnings."""
        self.user.register_user()
        self.assertEqual(self.user.monthly_earnings, 5000.0)
        self.assertIn("User test_user registered successfully.", mock_stdout.getvalue())
    
    def test_calculate_balance_no_expenses(self):
        """Test balance calculation with no expenses."""
        self.user.monthly_earnings = 3000
        self.assertEqual(self.user.calculate_balance(), 3000)
    
    def test_calculate_balance_with_expenses(self):
        """Test balance calculation with expenses."""
        self.user.monthly_earnings = 4000
        self.user.expenses = {"rent": 1500, "food": 500}
        self.assertEqual(self.user.calculate_balance(), 2000)
    
    @patch('builtins.input', side_effect=["200", "Food"])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_expense_new_category(self, mock_stdout, mock_input):
        """Test adding an expense to a new category."""
        self.user.want_add_expenses()
        self.assertEqual(self.user.expenses["food"], 200)
        self.assertIn("Added expense of $200.00 for food.", mock_stdout.getvalue())
    
    @patch('builtins.input', side_effect=["300", "Food"])
    def test_add_expense_existing_category(self, mock_input):
        """Test adding an expense to an existing category."""
        self.user.expenses["food"] = 200
        self.user.want_add_expenses()
        self.assertEqual(self.user.expenses["food"], 500)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_information(self, mock_stdout):
        """Test displaying user information."""
        self.user.username = "test_user"
        self.user.monthly_earnings = 4000
        self.user.expenses = {"rent": 1500, "food": 500}
        self.user.display_information()
        output = mock_stdout.getvalue()
        self.assertIn("User: test_user", output)
        self.assertIn("Monthly Earnings: $4000.00", output)
        self.assertIn("rent: $1500.00", output)
        self.assertIn("food: $500.00", output)
        self.assertIn("Remaining Balance: $2000.00", output)

if __name__ == "__main__":
    unittest.main()
