'''
Created on 2 nov. 2021

:author: Hubert Degaudenzi
'''

from ElementsEnv.PathStripper import stripPath

import os
import unittest

from ElementsEnv.Temporary import TempDir


def touch(file_path):
    with open(file_path, 'a'):
        os.utime(file_path, None)


class PathStripperTest(unittest.TestCase):

    def _addDirs(self, dir_names, make=True):
        for n in dir_names:
            n_full_path = self._tmp_dir.getName(n)
            self._path_list.append(n_full_path)
            if make and not os.path.exists(n_full_path):
                os.mkdir(n_full_path)

    def _addFiles(self, dir_names, file_names):
        self._addDirs(dir_names)
        for d in dir_names:
            for f in file_names:
                stem = os.path.join(d, f)
                f_path = self._tmp_dir.getName(stem)
                touch(f_path)

    def setUp(self):
        unittest.TestCase.setUp(self)

        self._tmp_dir = TempDir()
        self._path_list = []

        self._addDirs(["dir1", "dir2", "dir3"])
        self._addDirs(["dir4"], make=False)
        self._addDirs(["dir5"])
        self._addDirs(["dir6"], make=False)
        self._addDirs(["dir7"])

        self._addDirs(["dir1", "dir2", "dir3"], make=False)
        self._addDirs(["dir8"])

        self._addFiles(["dir3", "dir8"], ["file1", "file2", "file3", ])

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testStripPath(self):

        path_value = os.pathsep.join(self._path_list)

        non_empty_ref_path_list = []

        for n in ["dir3", "dir8"]:
            non_empty_ref_path_list.append(self._tmp_dir.getName(n))

        self.assertEqual(os.pathsep.join(non_empty_ref_path_list), stripPath(path_value))

        self.assertNotEqual("", stripPath(path_value, exist_only=True))

        ref_path_list = []

        for n in ["dir1", "dir2", "dir3", "dir5", "dir7", "dir8"]:
            ref_path_list.append(self._tmp_dir.getName(n))

        self.assertEqual(os.pathsep.join(ref_path_list), stripPath(path_value, exist_only=True))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testStripPath']
    unittest.main()
