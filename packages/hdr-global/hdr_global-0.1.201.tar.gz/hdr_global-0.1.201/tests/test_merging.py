from resources.hdr_merge import merging
from resources.crfio import CRF_importer
import unittest
import pickle
import numpy
import cv2


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


class TestMerging(unittest.TestCase):

    def test_merging(self):
        # Load the expected inputs and outputs
        images_w_exposure = load_pickle('examplers/pickles/list_10.pkl')
        expected_output = load_pickle('examplers/pickles/merge.pkl')
        crf = load_pickle('examplers/pickles/crf.pkl')

        # Call the function with the expected inputs
        result = merging(images_w_exposure, crf)

        # Check the function output
        self.assertTrue(numpy.array_equal(result, expected_output))

if __name__ == '__main__':
    unittest.main()