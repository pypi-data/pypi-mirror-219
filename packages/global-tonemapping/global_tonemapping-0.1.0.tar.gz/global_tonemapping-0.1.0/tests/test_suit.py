import unittest
from tests.test_crfio import TestCRFExportImport
from tests.test_merging import TestMerging
from tests.test_tonemap import TestTonemap
from tests.test_sharpen import TestSharpen
from tests.test_processor import TestProcessor

from examplers.create_pickles_dict import create_pickles_dict
from examplers.create_pickles_list import create_pickle_list
from examplers.create_merge import create_merge_pickle
from examplers.create_tonemap import create_tonemap_pickle
from examplers.create_sharpen import create_sharpen_pickle

def custom_test_suite():
    suite = unittest.TestSuite()

    # Add tests in a specific order
    suite.addTest(unittest.makeSuite(TestCRFExportImport))
    suite.addTest(unittest.makeSuite(TestMerging))
    suite.addTest(unittest.makeSuite(TestTonemap))
    suite.addTest(unittest.makeSuite(TestSharpen))
    suite.addTest(unittest.makeSuite(TestProcessor))

    return suite

if __name__ == '__main__':
    create_pickles_dict(output='./examplers/pickles/dict.pkl')
    create_pickle_list(input='./examplers/pickles/dict.pkl', output='./examplers/pickles/image_w_exposure.pkl')
    create_merge_pickle(input='./examplers/pickles/image_w_exposure.pkl', output='./examplers/pickles/merged.pkl')
    create_tonemap_pickle(input='./examplers/pickles/merged.pkl', output='./examplers/pickles/tonemap.pkl')
    create_sharpen_pickle(input='./examplers/pickles/tonemap.pkl', output='./examplers/pickles/sharpen.pkl')

    runner = unittest.TextTestRunner()
    runner.run(custom_test_suite())