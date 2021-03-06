""" Ensure that we are testing the right files. The ones that are
    located in the neighbour python directory
"""

import ElementsEnv

import unittest
import os


class LocationTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testElementsEnvLocation(self):
        imported_dir = os.path.dirname(ElementsEnv.__file__)
        tests_dir = os.path.dirname(__file__)
        main_dir = os.path.dirname(tests_dir)
        target_dir = os.path.join(main_dir, "python", "ElementsEnv")
        self.assertEqual(imported_dir, target_dir,
                         "Please setup the right python runtime environment: %s != %s" % (imported_dir, target_dir))


if __name__ == '__main__':
    unittest.main()
