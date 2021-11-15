'''
Created on 15 nov. 2021

:author: Hubert Degaudenzi
'''

from ElementsEnv.Version import stringVersion2Tuple

import unittest


class VersionTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testString2Tuple(self):

        ver_string = "2.1.3"
        ref_tuple = (2, ".", 1, ".", 3)
        ref_numbers = (2, 1, 3)

        self.assertEqual(stringVersion2Tuple(ver_string), ref_tuple)
        self.assertEqual(stringVersion2Tuple(ver_string, only_numbers=True),
                         ref_numbers)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
