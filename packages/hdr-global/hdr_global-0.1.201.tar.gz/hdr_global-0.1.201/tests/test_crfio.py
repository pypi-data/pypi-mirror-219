import unittest
import os
import numpy as np
from resources import crfio


class TestCRFExportImport(unittest.TestCase):
    def setUp(self):
        """Setup a dummy CRF and a file path."""
        self.crf = np.array([1, 2, 3, 4, 5])  # Dummy CRF.
        self.path = "../config/test.npy"  # Temporary path for the test.

    def test_export_import(self):
        """Test the exporter and importer functions."""
        crfio.CRF_exporter(self.crf, self.path)

        # Assert that the file was created.
        self.assertTrue(os.path.exists(self.path), "File not created by exporter")

        loaded_crf = crfio.CRF_importer(self.path)

        # Assert that the loaded CRF matches the original one.
        np.testing.assert_array_equal(loaded_crf, self.crf, "Loaded CRF doesn't match original CRF")

        print("Both the tests passed successfully.")

    def tearDown(self):
        """Cleanup the created file after tests."""
        if os.path.exists(self.path):
            os.remove(self.path)


if __name__ == "__main__":
    unittest.main()