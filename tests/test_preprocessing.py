import unittest
from src.data.preprocessing import clean_data, normalize_data, split_data

class TestDataPreprocessing(unittest.TestCase):

    def test_clean_data(self):
        # Test case for cleaning data
        raw_data = {'column1': [1, None, 3], 'column2': ['a', 'b', None]}
        cleaned_data = clean_data(raw_data)
        expected_data = {'column1': [1, 3], 'column2': ['a', 'b']}
        self.assertEqual(cleaned_data, expected_data)

    def test_normalize_data(self):
        # Test case for normalizing data
        data = [1, 2, 3, 4, 5]
        normalized_data = normalize_data(data)
        expected_data = [0, 0.25, 0.5, 0.75, 1]
        self.assertEqual(normalized_data, expected_data)

    def test_split_data(self):
        # Test case for splitting data
        data = [1, 2, 3, 4, 5]
        train_data, test_data = split_data(data, test_size=0.2)
        self.assertEqual(len(train_data), 4)
        self.assertEqual(len(test_data), 1)

if __name__ == '__main__':
    unittest.main()