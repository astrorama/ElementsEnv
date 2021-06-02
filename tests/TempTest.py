from ElementsEnv.Temporary import TempDir
import os

import unittest


class TestCase(unittest.TestCase):

    """ test case for the temporary directory class """

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.samplebasename = "toto"
        self.tmpdir = TempDir(suffix="tempdir", prefix=self.samplebasename)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testName(self):
        name1 = str(self.tmpdir)
        name2 = self.tmpdir.getName()
        # the next line should print twice the same thing
        self.assertEqual(name1, name2)

    def testDestruction(self):
        mydir = TempDir(suffix="tempdir", prefix="mydir")
        mydirname = mydir.getName()
        del mydir
        # the temporary directory should have been removed
        self.assertFalse(os.path.exists(mydirname))


if __name__ == '__main__':
    unittest.main()
