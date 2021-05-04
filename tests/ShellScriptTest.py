import os
import subprocess as sp
import pytest
from glob import glob

def collect_files():
    '''
    Collects all the files with a particular extension from the current working directory
    :param extension: extension of files that are to be collected
    :return: list containing all the names of files with a given extension
    '''

    file_list = []

    parent_dir = os.path.dirname(__file__)

    tst_list = glob(os.path.join(parent_dir, "*"))

    file_list = [f for f in tst_list if not os.path.splitext(f)[1] and not os.path.isdir(f)]

    return file_list

def test_shell_scripts(file_list = collect_files()):
    '''
    Tests all the shell scripts based on its exit code
    :param file_list: contains files that are to be tested
    :return: exitcode of each file
    '''
    returncode_list = []
    for each_script in file_list:

        returncode = sp.call(each_script, shell=True)
        returncode_list.append(returncode)


    for i in range(len(file_list)):
        assert(returncode_list[i] == 0),"Test Failed for " + file_list[i]
        print("test passed for " + file_list[i])


