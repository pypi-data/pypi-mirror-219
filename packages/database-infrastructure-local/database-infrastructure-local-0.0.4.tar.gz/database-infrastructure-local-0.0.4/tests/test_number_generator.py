import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
load_dotenv()
from CirclesNumberGenerator.number_generator import NumberGenerator

class TestNumberGenerator(unittest.TestCase):
    
    def setUp(self):
        self.num_gen = NumberGenerator("profile", "profile_table")

    def test_number_generator(self):
        conn = self.num_gen.db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT `number` FROM profile_table")
        
        existing_numbers = cursor.fetchall()
        
        for i in range(10):
            num = self.num_gen.get_random_number()
            assert num not in existing_numbers

if __name__ == '__main__':
    unittest.main()