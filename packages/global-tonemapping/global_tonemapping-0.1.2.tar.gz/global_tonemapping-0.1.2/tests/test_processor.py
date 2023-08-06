from resources.crfio import CRF_importer
from resources.hdr_merge import merging
from resources.ldr_sharpen import LDR_sharpen
from resources.tonemaping import tonemaping
from processor import processor
import numpy.testing as npt

import pickle
import unittest
import pickle
import numpy
import cv2


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

class TestProcessor(unittest.TestCase):
    def test_processor_b(self):
        input = load_pickle('./examplers/pickles/list_10.pkl')
        expected_output = load_pickle('./examplers/pickles/sharpen.pkl')
        # Call the function with the expected inputs
        result = processor(input, selector="B", gamma=1.4, saturation=2.0, sharpening_iteration=3, s=20, r=0.1)

        # Check the function output
        self.assertTrue(numpy.array_equal(result, expected_output))


    def test_processor_b_v2(self):
        input = load_pickle('./examplers/pickles/dict_10.pkl')
        expected_output = load_pickle('./examplers/pickles/sharpen.pkl')
        # Call the function with the expected inputs
        result = processor(input, selector="B", gamma=1.4, saturation=2.0, sharpening_iteration=3, s=20, r=0.1)

        try:
            npt.assert_array_equal(result, expected_output)
        except AssertionError as e:
            print(f'Test_processor_b failed with difference: {e}')
            raise

    def test_processor_b_crf(self):
        input = load_pickle('./examplers/pickles/list_100.pkl')
        expected_output = load_pickle('./examplers/pickles/crf.pkl')
        # Call the function with the expected inputs
        result = processor(input, selector="B", gamma=1.4, saturation=2.0, sharpening_iteration=3, s=20, r=0.1, mode="calibration")

        # Check the function output
        self.assertTrue(numpy.array_equal(result, expected_output))

    def test_processor_b_v2_crf(self):
        input = load_pickle('./examplers/pickles/list_100.pkl')
        expected_output = load_pickle('./examplers/pickles/crf.pkl')
        # Call the function with the expected inputs
        result = processor(input, selector="B", gamma=1.4, saturation=2.0, sharpening_iteration=3, s=20, r=0.1, mode="calibration")

        try:
            npt.assert_array_equal(result, expected_output)
        except AssertionError as e:
            print(f'Test_processor_b failed with difference: {e}')
            raise

if __name__ == '__main__':
    unittest.main()