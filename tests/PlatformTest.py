from Euclid.Platform import NativeMachine, getBinaryOfType, getBinaryTypeName
from Euclid.Platform import isBinaryType
from Euclid.Platform import getSearchList

import unittest


class PlatformTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testFlavour(self):
        machine = NativeMachine()
        print(machine.OSVersion())
        print(machine.CMTSystem())
        print(machine.binaryOSFlavour())
        print(machine.OSEquivalentFlavour())
        print(machine.compatibleBinaryTag())
        print(machine.compatibleBinaryTag(all_types=True))
        print(machine.supportedBinaryTag())
        print(machine.supportedBinaryTag(all_types=True))
        print(machine.nativeCompilerName())
        print(machine.nativeCompilerVersion())
        print(machine.nativeCompiler())
        print(machine.nativeBinaryTag())
        print(machine.nativeBinaryTag("Debug"))
        print("================================================================")
        self.assertEqual(machine.OSFlavour(
            teststring="Scientific Linux CERN SLC release 5.4 (Boron)"), "Scientific Linux")
        self.assertEqual(machine.OSVersion(), "5.4")
        print(machine.binaryOSFlavour())
        print(machine.OSEquivalentFlavour())
        print(machine.compatibleBinaryTag())
        print(machine.compatibleBinaryTag(all_types=True))
        print(machine.supportedBinaryTag())
        print(machine.supportedBinaryTag(all_types=True))
        print(machine.nativeCompilerVersion())
        print(machine.nativeCompiler())
        print(machine.nativeBinaryTag())
        print(machine.nativeBinaryTag("Debug"))

    def testBinaryType(self):
        self.assertTrue(isBinaryType("x86_64-fc20-gcc48-dbg", "Debug"))
        self.assertFalse(isBinaryType("x86_64-fc20-gcc48-opt", "Debug"))
        self.assertFalse(isBinaryType("x86_64-fc20-gcc48-dbg", "Release"))
        self.assertTrue(isBinaryType("x86_64-fc20-gcc48-opt", "Release"))

    def testConvertBinaryType(self):
        self.assertEqual(
            getBinaryOfType("x86_64-fc20-gcc48-dbg", "Debug"), "x86_64-fc20-gcc48-dbg")
        self.assertEqual(
            getBinaryOfType("x86_64-fc20-gcc48-opt", "Debug"), "x86_64-fc20-gcc48-dbg")
        self.assertEqual(
            getBinaryOfType("x86_64-fc20-gcc48-dbg", "Release"), "x86_64-fc20-gcc48-opt")
        self.assertEqual(
            getBinaryOfType("x86_64-fc20-gcc48-opt", "Release"), "x86_64-fc20-gcc48-opt")

        self.assertEqual(getBinaryOfType(
            "x86_64-fc20-gcc48-dbg", "RelWithDebInfo"), "x86_64-fc20-gcc48-o2g")
        self.assertEqual(getBinaryOfType(
            "x86_64-fc20-gcc48-opt", "RelWithDebInfo"), "x86_64-fc20-gcc48-o2g")

    def testTypeName(self):
        self.assertEqual(getBinaryTypeName("x86_64-fc20-gcc48-dbg"), "Debug")
        self.assertEqual(getBinaryTypeName("x86_64-fc20-gcc48-opt"), "Release")
        self.assertEqual(
            getBinaryTypeName("x86_64-fc20-gcc48-cov"), "Coverage")
        self.assertEqual(getBinaryTypeName("x86_64-fc20-gcc48-pro"), "Profile")
        self.assertEqual(
            getBinaryTypeName("x86_64-fc20-gcc48-o2g"), "RelWithDebInfo")
        self.assertEqual(
            getBinaryTypeName("x86_64-fc20-gcc48-min"), "MinSizeRel")

        self.assertEqual(getBinaryTypeName("dbg"), "Debug")
        self.assertEqual(getBinaryTypeName("opt"), "Release")
        self.assertEqual(getBinaryTypeName("cov"), "Coverage")
        self.assertEqual(getBinaryTypeName("pro"), "Profile")
        self.assertEqual(getBinaryTypeName("o2g"), "RelWithDebInfo")
        self.assertEqual(getBinaryTypeName("min"), "MinSizeRel")

    def testSearchBinaryList(self):
        ref_list = ["x86_64-fc20-gcc48-cov",
                    "x86_64-fc20-gcc48-o2g",
                    "x86_64-fc20-gcc48-opt",
                    "x86_64-fc20-gcc48-dbg",
                    "x86_64-fc20-gcc48-pro",
                    "x86_64-fc20-gcc48-min"
                    ]
        search_list = getSearchList("x86_64-fc20-gcc48-cov")
        self.assertEqual(search_list, ref_list)

    def testVersion(self):
        pass


if __name__ == '__main__':
    unittest.main()
