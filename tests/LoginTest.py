from Euclid.Login import getLoginEnv, getLoginAliases, getLoginExtra
from Euclid.Login import DEFAULT_BUILD_TYPE

import unittest
import os


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testDefaultBinaryTag(self):
        env = getLoginEnv()
        self.assertTrue(env["BINARY_TAG"].endswith("-o2g"))

    def testBinaryTagReUse(self):
        os.environ["BINARY_TAG"] = "x86_64-fc20-gcc48-dbg"
        env = getLoginEnv(["--silent"])
        self.assertEqual(env["BINARY_TAG"], "x86_64-fc20-gcc48-dbg")
        del os.environ["BINARY_TAG"]

    def testForceBinaryTag(self):
        env = getLoginEnv(["-b", "x86_64-slc7-gcc48-min"])
#        self.assertEqual(env["BINARY_TAG"], "x86_64-slc7-gcc48-min")

    def testChooseBinaryType(self):
        env = getLoginEnv(["Release"])
        self.assertTrue(env["BINARY_TAG"].endswith("-opt"))
        env = getLoginEnv(["release"])
        self.assertTrue(env["BINARY_TAG"].endswith("-opt"))
        env = getLoginEnv(["RelWithDebInfo"])
        self.assertTrue(env["BINARY_TAG"].endswith("-o2g"))
        env = getLoginEnv(["dbg"])
        self.assertTrue(env["BINARY_TAG"].endswith("-dbg"))

    def testAlias(self):
        al = getLoginAliases()
        self.assertEqual(al["ERun"], "E-Run")
        self.assertEqual(al["EuclidRun"], "E-Run")


if __name__ == '__main__':
    unittest.main()
