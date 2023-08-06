import unittest
from tests.test_crfio import TestCRFExportImport
from tests.test_merging import TestMerging
from tests.test_tonemap import TestTonemap
from tests.test_sharpen import TestSharpen
from tests.test_processor import TestProcessor
from tests.test_crf_calc import TestCRFCalc

def custom_test_suite():
    suite = unittest.TestSuite()

    # Add tests in a specific order
    suite.addTest(unittest.makeSuite(TestCRFExportImport))
    suite.addTest(unittest.makeSuite(TestMerging))
    suite.addTest(unittest.makeSuite(TestTonemap))
    suite.addTest(unittest.makeSuite(TestSharpen))
    suite.addTest(unittest.makeSuite(TestProcessor))
    suite.addTest(unittest.makeSuite(TestCRFCalc))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(custom_test_suite())