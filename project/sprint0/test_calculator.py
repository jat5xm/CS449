import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        # This method is called before each test
        self.calc = Calculator()

    def tearDown(self):
        # This method is called after each test
        pass

    # Test case 1: Testing the add function
    def test_add(self):
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)

    # Test case 2: Testing the subtract function
    def test_subtract(self):
        result = self.calc.subtract(5, 3)
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
