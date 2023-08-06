from resources import ldr_sharpen
import unittest
import pickle
import numpy
import cv2


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

class TestSharpen(unittest.TestCase):

    def test_sharpen_b(self):
        tonemap = load_pickle('examplers/pickles/tonemap.pkl')
        expected_output = load_pickle('examplers/pickles/sharpen.pkl')
        # Call the function with the expected inputs
        result = ldr_sharpen.LDR_sharpen(tonemap)

        # Check the function output
        self.assertTrue(numpy.array_equal(result, expected_output))

if __name__ == '__main__':
    unittest.main()