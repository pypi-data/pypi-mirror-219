from resources.hdr_merge import merging
from resources.crf_calc import CRF_calculate
import unittest
import pickle
import numpy
import cv2

def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

class TestCRFCalc(unittest.TestCase):
    def setUp(self):
        self.input = './examplers/pickles/list_100.pkl'
        self.output = './examplers/pickles/crf.pkl'

    def test_crf_calc(self):
        images_w_exposure = load_pickle(self.input)
        expected_output = load_pickle(self.output)

        result = CRF_calculate(images_w_exposure)

        # Check the function output
        self.assertTrue(numpy.array_equal(result, expected_output))


if __name__ == '__main__':
    unittest.main()