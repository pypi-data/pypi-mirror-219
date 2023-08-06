from resources import tonemaping
import unittest
import pickle
import numpy
import cv2



def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

class TestTonemap(unittest.TestCase):
    def test_tonemap(self):
        tonemap = load_pickle("examplers/pickles/merge.pkl")
        expected_output = load_pickle("examplers/pickles/tonemap.pkl")

        result = tonemaping.tonemaping(tonemap)

        # Check the function output
        self.assertTrue(numpy.array_equal(result, expected_output))
if __name__ == '__main__':
    unittest.main()