from Euclid.Path import multiPathJoin, multiPathUpdate, cleanPath
from Euclid.Path import pathRemove, hasCommand
from Euclid.Path import upWalk, getClosestPath

from Euclid.Temporary import TempDir

import unittest
import os


class PathTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.tpath = "mysiteroot1:mysiteroot2"
        self.sub1 = "lhcb"
        self.sub2 = os.path.join("lcg", "external")

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testMultiJoin(self):
        self.assertEqual(
            multiPathJoin(self.tpath, self.sub1), "mysiteroot1/lhcb:mysiteroot2/lhcb")
        self.assertEqual(multiPathJoin(self.tpath, self.sub2),
                         "mysiteroot1/lcg/external:mysiteroot2/lcg/external")

    def testMultiUpdate(self):
        self.assertEqual(multiPathUpdate(self.tpath, [self.sub1, self.sub2]),
                         "mysiteroot1/lhcb:mysiteroot2/lhcb:mysiteroot1/lcg/external:mysiteroot2/lcg/external")
        self.assertEqual(multiPathUpdate(self.tpath, [self.sub1, self.sub2], interleaved=False),
                         "mysiteroot1/lhcb:mysiteroot2/lhcb:mysiteroot1/lcg/external:mysiteroot2/lcg/external")
        self.assertEqual(multiPathUpdate(self.tpath, [self.sub1, self.sub2], interleaved=True),
                         "mysiteroot1/lhcb:mysiteroot1/lcg/external:mysiteroot2/lhcb:mysiteroot2/lcg/external")

    def testCleanPath(self):
        p1 = "/dab//blu//"
        self.assertEqual(cleanPath(p1), "/dab//blu")
        self.assertEqual(cleanPath(p1, normalize=True), "/dab/blu")
        p2 = "//dab//blu//"
        self.assertEqual(cleanPath(p2, normalize=True), "//dab/blu")
        p3 = "/dab/blu/df:"
        self.assertEqual(cleanPath(p3, normalize=True), "/dab/blu/df")
        p4 = "/dab/blu/df::"
        self.assertEqual(cleanPath(p4, normalize=True), "/dab/blu/df")
        p5 = "/dab/blu/df://tra:"
        self.assertEqual(cleanPath(p5, normalize=True), "/dab/blu/df://tra")
        p6 = ":/dab/blu/df:://tra:foo:bar/ssd/../bli"
        self.assertEqual(
            cleanPath(p6, normalize=True), "/dab/blu/df://tra:foo:bar/bli")
        p7 = ":/dab/blu/df:://tra:foo:bar/ssd/../bli"
        self.assertEqual(cleanPath(p7), "/dab/blu/df://tra:foo:bar/ssd/../bli")

    def testPathRemove(self):
        p1 = "/opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v6r3/InstallArea/scripts:/opt/LHCb/lib/lcg/external/Python/2.6.5/x86_64-slc5-gcc43-opt/bin:/opt/LHCb/lib/lcg/external/gcc/4.3.2/x86_64-slc5/bin:/opt/LHCb/lib/lhcb/COMPAT/COMPAT_v1r8/CompatSys/x86_64-slc5-gcc43-opt/bin:/opt/LHCb/lib/contrib/CMT/v1r20p20090520/Linux-x86_64"
        cmpt = ["lcg", "external", "Python"]
        result = "/opt/LHCb/lib/lhcb/LBSCRIPTS/LBSCRIPTS_v6r3/InstallArea/scripts:/opt/LHCb/lib/lcg/external/gcc/4.3.2/x86_64-slc5/bin:/opt/LHCb/lib/lhcb/COMPAT/COMPAT_v1r8/CompatSys/x86_64-slc5-gcc43-opt/bin:/opt/LHCb/lib/contrib/CMT/v1r20p20090520/Linux-x86_64"
        self.assertEqual(pathRemove(p1, cmpt), result)

    def testHasCommand(self):
        self.assertFalse(hasCommand("ddkfhd"))
        self.assertTrue(hasCommand("python"))

    def testUpWalk(self):
        p1 = "/usr/local/bin"
        l1 = ['/usr/local/bin', '/usr/local', '/usr', '/']

        l = [r for r, d, o in upWalk(p1)]

        self.assertEqual(l1, l)

    def testGetClosestPath(self):
        t = TempDir()
        os.mkdir(os.path.join(t.getName(), "usr"))
        os.mkdir(os.path.join(t.getName(), "usr", "bin"))
        os.mkdir(os.path.join(t.getName(), "usr", "local"))
        os.mkdir(os.path.join(t.getName(), "usr", "local", "bin"))

        l1 = []
        l1.append(os.path.join(t.getName(), "usr", "local", "bin"))
        l1.append(os.path.join(t.getName(), "usr", "bin"))
        if os.path.exists(os.path.join(t.getName(), "bin")):
            l1.append(os.path.join(t.getName(), "bin"))
        if os.path.exists(os.path.join("/tmp", "bin")):
            l1.append(os.path.join("/tmp", "bin"))
        l1.append(os.path.join(os.sep + "bin"))

        ttop = os.path.join(t.getName(), "usr", "local", "bin", "toto")

        l = [p for p in getClosestPath(ttop, "bin", alloccurences=True)]

        self.assertEqual(l1, l)

        l3 = []
        l3.append(os.path.join(t.getName(), "usr", "local", "bin"))

        r = [p for p in getClosestPath(ttop, "bin", alloccurences=False)]

        self.assertEqual(l3, r)

        l4 = []

        s = [p for p in getClosestPath(ttop, "djldfdhf", alloccurences=False)]

        self.assertEqual(l4, s)


if __name__ == '__main__':
    unittest.main()
