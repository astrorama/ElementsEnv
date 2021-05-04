
import sys
assert sys.version_info >= (2, 6), "Python >= 2.6 is required"


def _defaultPath():
    '''
    Return the default search path, based on the variables CMAKE_PREFIX_PATH and
    CMAKE_PROJECT_PATH.
    '''
    import os
    env_vars = ['EUCLIDPROJECTPATH']
    is_set = lambda v: os.environ.get(v)
    var2path = lambda v: os.environ[v].split(os.pathsep)
    return sum(map(var2path, filter(is_set, env_vars)), [])

path = _defaultPath()


class Error(RuntimeError):

    '''
    Base class for ERun exceptions.
    '''


def execute(project, command, version="latest"):
    pass
