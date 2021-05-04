import re
import os


def isValidSimpleVersion(version):
    '''
    Check if the specified version number is a valid one for the project. 
    '''
    return (re.match(r"^v[0-9]+r[0-9]+(p[0-9]+)?(g[0-9]+)?$", version)
            or re.match(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$", version)
            )


def isValidVersion(project, version):
    '''
    Check if the specified version number is a valid (reasonable) one for the
    specified project. "latest" and "HEAD" are allowed.
    '''
    # FIXME: for the moment we accept only some simple values, but we should
    # look for aliases too
    return (version.lower() in ('latest', 'head') or isValidSimpleVersion(version))


def expandVersionAlias(project, version):
    '''
    Given a project and a version, check if the version is an alias for an
    explicit version (e.g. latest, reco19) and return the real version or the argument.
    '''
    # FIXME: for the moment there is no mechanism to store version aliases
    return version


def getVersionDirs(project_path, suffix=None, valid_function=isValidSimpleVersion):
    '''
    Get the list of version that correspond to the subdirectories of the project
    with optionally a valid version and optionally the correct suffix path
    '''
    version_list = []
    sub_dirs = os.listdir(project_path)
    for s in sub_dirs:
        keep = False
        if valid_function:
            if valid_function(s):
                keep = True
        else:
            keep = True
        if keep:
            full_s = os.path.join(project_path, s)
            if suffix:
                full_s = os.path.join(full_s, suffix)
            if os.path.exists(full_s):
                version_list.append(s)

    return version_list


def stringVersion2Tuple(strver):
    """ convert string into a tuple of number and strings """
    sl = re.split("(\d+)", strver)
    nsl = []
    for i in sl:
        if i:
            if re.match("\d+", i):
                nsl.append(int(i))
            else:
                nsl.append(i)
    return tuple(nsl)


def versionSort(strlist, reverse=False):
    """ Generic sorting of strings containing numbers aka versions """
    versionlist = [(stringVersion2Tuple(str(s)), s) for s in strlist]
    versionlist.sort()
    if reverse:
        versionlist.reverse()
    return [x[1] for x in versionlist]
