""" Elements version style definition and massaging """
# $Id$

from fnmatch import fnmatch
from past.builtins import cmp

import re
import os

# This is the version style used in the releases: vXrY[pZ]
_txt_version_style = r'v([0-9]+)r([0-9]+)(?:p([0-9]+))?(?:g([0-9]+))?'
version_style = re.compile(_txt_version_style)

# This is the version style for the LCGCMT releases: 56[a]
_txt_lcg_version_style = r'([0-9]+)([a-z]?)'
lcg_version_style = re.compile(_txt_lcg_version_style)

# user version style : hmd_091008
_txt_user_cvs_version_style = r'(?:\w+_([0-9]{4})([0-9]{2})([0-9]{2})[a-z]?)'
user_cvs_version_style = re.compile(_txt_user_cvs_version_style)

# full version style used in CVS: the regular style with the possible
# "pre" suffix or the user ones.
_txt_cvs_version_style = r'%s(?:-pre([0-9]+))?|%s' % (
    _txt_version_style, _txt_user_cvs_version_style)

cvs_version_style = re.compile(_txt_cvs_version_style)


class NotAVersion(Exception):
    pass


class GenericVersion(object):
    txt_version_style = None
    version_style = None

    def __init__(self, vname):
        self._vname = vname
        if vname:
            self._version = stringVersion2Tuple(vname)
        else:
            self._version = vname
        self._patchversion = False

    def __str__(self):
        return self._vname

    def __repr__(self):
        return "%s %s" % (self.__class__, self._vname)

    def __cmp__(self, other):
        return cmp(self._version, other.version())

    def __hash__(self):
        return hash(self._vname)

    def name(self):
        return self._vname

    def version(self):
        return self._version


class CoreVersion(GenericVersion):
    txt_version_style = _txt_version_style
    version_style = re.compile("%s$" % _txt_version_style)

    def __init__(self, vname):
        super(CoreVersion, self).__init__(vname)
        try:
            m = self.version_style.match(self._vname)
        except TypeError:
            raise NotAVersion(vname)
        if m:
            a, b, c, d = m.groups()
            if a is None or b is None:
                raise NotAVersion(vname)
            a = int(a)
            b = int(b)
            if c is not None:
                self._patchversion = True
                c = int(c)
            if d is not None:
                self._parallelversion = True
                d = int(d)
            self._version = (a, b, c, d)
        else:
            raise NotAVersion(vname)


class LCGVersion(GenericVersion):
    txt_version_style = _txt_lcg_version_style
    version_style = re.compile("%s$" % _txt_lcg_version_style)

    def __init__(self, vname):
        super(LCGVersion, self).__init__(vname)
        try:
            m = self.version_style.match(self._vname)
        except TypeError:
            raise NotAVersion(vname)
        if m:
            a, b = m.groups()
            if a is None:
                raise NotAVersion(vname)
            a = int(a)
            self._version = (a, b)
        else:
            raise NotAVersion(vname)


def sortVersions(versionlist, versiontype=CoreVersion, safe=False, reverse=False):
    if not safe:
        vlist = [versiontype(x) for x in versionlist]
    else:
        vlist = []
        for v in versionlist:
            try:
                v = versiontype(v)
            except NotAVersion:
                continue
            vlist.append(v)
    vlist.sort()
    if reverse:
        vlist.reverse()
    return [x.name() for x in vlist]


def extractVersion(strname, versiontype=CoreVersion):
    result = None
    if versiontype and versiontype.txt_version_style:
        verstyle = re.compile(versiontype.txt_version_style)
        m = verstyle.search(strname)
        if m:
            result = versiontype(m.group())
    else:
        result = GenericVersion(strname)
    return result


def sortStrings(strlist, versiontype=CoreVersion, safe=False, reverse=False):
    if versiontype:
        versionlist = [(extractVersion(s, versiontype=versiontype), s)
                       for s in strlist]
    else:
        versionlist = [(stringVersion2Tuple(s), s) for s in strlist]
    if safe:
        versionlist = [t for t in versionlist if t[0]]
    versionlist.sort()
    if reverse:
        versionlist.reverse()
    return [x[1] for x in versionlist]


def getVersionsFromDir(dirname, pattern=None, versiontype=CoreVersion, reverse=False):
    strlist = []
    for o in os.listdir(dirname):
        if pattern:
            if fnmatch(o, pattern):
                strlist.append(o)
        else:
            strlist.append(o)
    versionlist = [extractVersion(s, versiontype=versiontype) for s in strlist]
    versionlist = [v for v in versionlist if v]
    versionlist.sort()
    if reverse:
        versionlist.reverse()
    return versionlist


def LHCb2CMT(project, version):
    """ coonvert LHCb project version to raw CMT version:
        DaVinci, v20r3 -> DAVINCI, DAVINCI_v20r3
    """
    cmtproj = project.upper()
    if version:
        cmtvers = "%s_%s" % (cmtproj, version)
    else:
        cmtvers = None

    return (cmtproj, cmtvers)


def ParseSvnVersion(svn_id, url=""):
    """
    Translate the SVN url of the file to a version number, if possible;
    return the id otherwise.
    Tipical usage:

    __version__ = ParseSvnVersion("$"""'Id'"""$", "$"""'URL'"""$")

    Remember to set the property 'svn:keywords' to 'Id URL' for the files that need it.

    Note: The URL must be of the approximate format ".*/tags.*/v\\d+r\\d+(p\\d+)?/.*".
    """
    m = re.search(r"\$[^$]*/tags.*/(\d+\.\d+(\.\d+)?)/[^$]* \$", url)
    if not m:
        return svn_id
    else:
        return m.group(1)


def stringVersion2Tuple(strver, only_numbers=False):
    """ convert string into a tuple of number and strings """
    sl = re.split(r"(\d+)", strver)
    nsl = []
    for i in sl:
        if i:
            if re.match(r"\d+", i):
                nsl.append(int(i))
            elif not only_numbers:
                nsl.append(i)
    return tuple(nsl)


def versionSort(strlist, reverse=False):
    """ Generic sorting of strings containing numbers aka versions """
    versionlist = [(stringVersion2Tuple(str(s)), s) for s in strlist]
    versionlist.sort()
    if reverse:
        versionlist.reverse()
    return [x[1] for x in versionlist]
