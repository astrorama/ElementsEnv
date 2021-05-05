""" General ElementsEnv platform configuration """

import sys
import platform
import os
import re
import logging

from subprocess import Popen, PIPE

from .Path import hasCommand

# CMake Build Types

DEFAULT_BUILD_TYPE = "RelWithDebInfo"

BUILD_TYPES = {
    "Release": "opt",
    "Debug": "dbg",
    "Coverage": "cov",
    "Profile": "pro",
    "RelWithDebInfo": "o2g",
    "MinSizeRel": "min"
}

CANONICAL_ORDER = [
    "RelWithDebInfo",
    "Release",
    "Debug",
    "Profile",
    "Coverage",
    "MinSizeRel"
    ]

# BINARY_TAG extraction


def isBinaryType(binary_tag, btype):
    """ check if the BINARY_TAG value is one from the type """
    bintype = True
    if not binary_tag.endswith("-%s" % BUILD_TYPES[btype]):
        bintype = False
    return bintype


def getBinaryOfType(binary_tag, btype):
    """ convert the BINARY_TAG to another type """
    btother = binary_tag
    if not isBinaryType(binary_tag, btype):
        blist = binary_tag.split("-")[:-1]
        blist.append(BUILD_TYPES[btype])
        btother = "-".join(blist)
    return btother


def getSearchList(binary_tag):
    """ return the list of search binary type
        with the first one being the default
     """
    search_list = [binary_tag]

    for local_t in CANONICAL_ORDER:
        new_binary_tag = getBinaryOfType(binary_tag, local_t)
        if new_binary_tag != binary_tag:
            search_list.append(new_binary_tag)

    return search_list


def getBinaryTypeName(binary_tag):
    """ Function to extract the binary type"""
    type_name = None
    for j in BUILD_TYPES:
        if binary_tag.endswith(BUILD_TYPES[j]):
            type_name = j

    return type_name


def getCompiler(binary_tag):
    """ extract compiler from BINARY_TAG """
    compdef = binary_tag.split("-")[2]
    return compdef


def getPlatformType(binary_tag):
    """ extract platform type (slc5, slc6, etc) from BINARY_TAG """
    platformtype = binary_tag.split("-")[1]
    if platformtype == "sl7":
        platformtype = "slc7"
    if platformtype == "sl6":
        platformtype = "slc6"
    if platformtype == "sl5":
        platformtype = "slc5"
    return platformtype


def getArchitecture(binary_tag):
    """ extract architecture from BINARY_TAG """
    architecture = binary_tag.split("-")[0]
    if architecture == "ia32":
        architecture = "i686"
    if architecture == "amd64":
        architecture = "x86_64"
    return architecture


def getBinaryTag(architecture, platformtype, compiler, binary_type=DEFAULT_BUILD_TYPE):
    binary_tag = None
    if platformtype.startswith("win"):
        if compiler:
            binary_tag = "_".join([platformtype, compiler])
            if compiler.startswith("vc9"):
                if architecture == "ia32":
                    architecture = "i686"
                elif architecture == "amd64":
                    architecture = "x86_64"
                binary_tag = "-".join([architecture, "winxp", compiler, "opt"])
        else:
            binary_tag = platformtype

    else:
        if architecture == "ia32":
            architecture = "i686"
        elif architecture == "amd64":
            architecture = "x86_64"
        if compiler:
            binary_tag = "-".join([architecture,
                                   platformtype, compiler, "opt"])
        else:
            binary_tag = "-".join([architecture, platformtype, "opt"])

    binary_tag = getBinaryOfType(binary_tag, binary_type)

    return binary_tag


# officially supported binaries
BINARY_OPT_LIST = ["x86_64-slc5-gcc43-opt", "i686-slc5-gcc43-opt",
                   "x86_64-slc5-gcc46-opt", "i686-slc5-gcc46-opt",
                   "win32_vc71", "i686-winxp-vc90-opt",
                   "x86_64-slc5-icc11-opt", "i686-slc5-icc11-opt",
                   "x86_64-slc6-gcc46-opt", "i686-slc6-gcc46-opt",
                   "x86_64-slc7-gcc48-opt", "i686-slc7-gcc48-opt",
                   "x86_64-co7-gcc48-opt", "i686-co7-gcc48-opt",
                   "x86_64-fc19-gcc48-opt", "i686-fc19-gcc48-opt",
                   "x86_64-fc20-gcc48-opt", "i686-fc20-gcc48-opt",
                   "x86_64-fc21-gcc49-opt", "i686-fc21-gcc49-opt",
                   "x86_64-fc22-gcc51-opt", "i686-fc22-gcc51-opt",
                   "x86_64-fc23-gcc53-opt", "i686-fc23-gcc53-opt",
                   "x86_64-fc24-gcc61-opt", "i686-fc24-gcc61-opt",
                   "x86_64-fc24-gcc62-opt", "i686-fc24-gcc62-opt",
                   "x86_64-fc24-gcc63-opt", "i686-fc24-gcc63-opt",
                   "x86_64-fc25-gcc63-opt", "i686-fc25-gcc63-opt",
                   "x86_64-fc32-gcc102-opt", "i686-fc32-gcc102-opt",
                   "x86_64-osx109-clang34-opt"
                   ]
# future possible supported binaries
EXTRA_BINARY_OPT_LIST = ["x86_64-slc5-gcc34-opt", "i686-slc5-gcc34-opt",
                         "i686-slc5-gcc43-opt",
                         "i686-winxp-vc90-opt", "x86_64-winxp-vc90-opt",
                         "osx105_ia32_gcc401", "x86_64-osx106-gcc42-opt"
                         ]

BINARY_TYPE_LIST = {}
EXTRA_BINARY_TYPE_LIST = {}
for t in BUILD_TYPES:
    BINARY_TYPE_LIST[t] = [getBinaryOfType(x, t) for x in BINARY_OPT_LIST]
    EXTRA_BINARY_TYPE_LIST[t] = [getBinaryOfType(x, t) for x in EXTRA_BINARY_OPT_LIST]

BINARY_DBG_LIST = BINARY_TYPE_LIST["Debug"]
EXTRA_BINARY_DBG_LIST = EXTRA_BINARY_TYPE_LIST["Debug"]

BINARY_LIST = []
EXTRA_BINARY_LIST = []
for t in BUILD_TYPES:
    BINARY_LIST.extend(BINARY_TYPE_LIST[t])
    EXTRA_BINARY_LIST.extend(EXTRA_BINARY_TYPE_LIST[t])

del t


def pathBinaryMatch(path, binary_tag):
    """ returns True if the path belong to the binary_tag distribution
    @param path: file/path to be tested
    @param binary_tag: target binary_tag
    """
    selected = False
    log = logging.getLogger()
    if binary_tag not in BINARY_LIST:
        log.error("the value of BINARY_TAG %s is not supported" % binary_tag)
    else:
        match_str = "%s" % binary_tag
        cfg_match = re.compile(match_str)
        if cfg_match.search(path):
            selected = True
    return selected


def pathSharedMatch(path, binary_tag=None):
    """ select path with are not part of a binary distribution
    @param path: file/dir path to be tested
    @param binary_tag: optional parameter to exclude specific files for a given binary_tag
    """
    selected = True
    for b in BINARY_LIST:
        if pathBinaryMatch(path, b):
            selected = False
            break
    return selected


def pathMatch(path, binary_tag, shared=False):
    """
    return True if the path belong to the BINARY_TAG.
    """
    selected = False
    if not shared:
        selected = pathBinaryMatch(path, binary_tag)
    else:
        selected = pathSharedMatch(path, binary_tag)
    return selected


def pathFilter(pathlist, binary_tag, shared=False):
    return [p for p in pathlist if pathMatch(p, binary_tag, shared)]


# supported shells
SUPPORTED_SHELLS = ["csh", "sh", "bat"]

# Native platform guessing

LINUX_RELEASE_FILES = ["/etc/redhat-release",
                       "/etc/system-release",
                       "/etc/SuSE-release",
                       "/etc/issue", "/etc/issue.net"]

LINUX_FLAVOUR_ALIASES = {
    "slc": ["Scientific Linux"],
    "rhel": ["Redhat Enterprise", "Red Hat Enterprise"],
    "rh": ["Redhat", "Red Hat"],
    "fc": ["Fedora", "Fedora Core"],
    "suse": ["SuSE"],
    "co": ["CentOS"],
    "deb": ["Debian"],
    "ub": ["Ubuntu"],
    "ml": ["Mandriva Linux"],
    "bb": ["Big Box Linux"]
}

LSB_FLAVOUR_ALIASES = {
    "sl": ["ScientificSL"],
    "slc": ["ScientificCERNSLC"],
    "fc": ["Fedora", "Fedora Core"],
    "co": ["CentOS"]
}

FLAVOUR_RUNTIME_COMPATIBILITY = {
    "slc7": ["slc7", "co7"],
    "co7": ["co7", "slc7"],
    "fc32": ["fc32", "fc25", "fc24", "fc23", "fc22", "fc21", "fc20", "fc19", "slc7"],
    "fc25": ["fc25", "fc24", "fc23", "fc22", "fc21", "fc20", "fc19", "slc7"],
    "fc24": ["fc24", "fc23", "fc22", "fc21", "fc20", "fc19", "slc7"],
    "fc23": ["fc23", "fc22", "fc21", "fc20", "fc19", "slc7"],
    "fc22": ["fc22", "fc21", "fc20", "fc19", "slc7"],
    "fc21": ["fc21", "fc20", "fc19", "slc7"],
    "fc20": ["fc20", "fc19", "slc7"],
    "fc19": ["fc19", "slc7"],
    "slc6": ["slc6", "slc5"],
    "slc5": ["slc5", "slc4"],
    "rh73": ["rh73"],
    "win32": ["win32"],
    "win64": ["win64"],
    "osx106": ["osx105", "osx106"]
}

ARCH_RUNTIME_COMPATIBILITY = {
    "x86_64": ["x86_64", "i686", "i586", "i486", "i386"],
    "ia64": ["ia64", "i686", "i586", "i486", "i386"],
    "ia32": ["ia32", "i686", "i586", "i486", "i386"],
    "i686": ["i686", "i586", "i486", "i386"],
    "i586": ["i586", "i486", "i386"],
    "i486": ["i486", "i386"],
    "i386": ["i386"],
    "ppc": ["ppc"]
}

FLAVOUR_RUNTIME_EQUIVALENCE = {
    "fc32": ["fc32"],
    "fc25": ["fc25"],
    "fc24": ["fc24"],
    "fc23": ["fc23"],
    "fc22": ["fc22"],
    "fc21": ["fc21"],
    "fc20": ["fc20"],
    "fc19": ["fc19"],
    "slc7": ["slc7"],
    "co7": ["co7"],
    "slc6": ["slc6"],
    "slc5": ["slc5", "co5", "rhel5", "ub9", "fc13", "fc12", "fc11", "fc10"],
    "rh73": ["rh73", "suse80", "suse81", "suse82", "suse83"],
    "win32": ["win32"],
    "win64": ["win64"],
    "osx106": ["osx106"]
}

# the first ones in the list have higher precedence
SUPPORTED_COMPILERS = {
    "fc32": ["gcc102"],
    "fc25": ["gcc63", "gcc62"],
    "fc24": ["gcc63", "gcc62", "gcc61"],
    "fc23": ["gcc53"],
    "fc22": ["gcc51"],
    "fc21": ["gcc49"],
    "fc20": ["gcc48"],
    "fc19": ["gcc48"],
    "slc7": ["gcc48"],
    "co7": ["gcc48"],
    "slc6": ["gcc46", "gcc45", "gcc44"],
    "slc5": ["gcc46", "gcc43", "gcc45", "icc11"],
    "win32": ["vc71", "vc9"],
    "win64": ["vc71", "vc9"],
    "osx106": ["gcc42"],
    "osx109": ["clang34"]
}


class NativeMachine:

    def __init__(self):
        """
        constructor
        """
        self._arch = None
        self._ostype = None
        self._machine = None
        self._osflavor = None
        self._osversion = None
        self._compversion = None
        self._compiler = None
        self._sysinfo = None
        self._lsb_distributor_id = None
        self._lsb_description = None
        self._lsb_release = None
        self._lsb_codename = None
        if hasattr(platform, "uname"):
            self._sysinfo = platform.uname()
        if sys.platform == "win32":
            self._arch = "32"
            self._ostype = "Windows"
            self._machine = "i686"
        elif sys.platform == "win64":
            self._arch = "64"
            self._ostype = "Windows"
            self._machine = "x86_64"
        else:
            self._ostype = self._sysinfo[0]
            self._machine = self._sysinfo[4]
            if self._ostype in ["Linux", "LynxOS", "Darwin"]:
                if self._machine == "x86_64" or self._machine == "ia64":
                    self._arch = "64"
                else:
                    self._arch = "32"
                if self._ostype == "Darwin" and Popen("uname -p", shell=True, stdout=PIPE, close_fds=True).communicate()[0].strip().decode("ascii") == "powerpc":
                    self._ostype = "ppc"

    def sysInfo(self):
        """ full platform.uname() list """
        return self._sysinfo

    def arch(self):
        """ returns 32 or 64 """
        return self._arch

    def OSType(self):
        """ returns Linux, Darwin, Windows """
        return self._ostype

    def machine(self):
        """ returns i386, i486, i686, x86_64, ia64, power mac """
        return self._machine

    def system(self):
        """ return Linux-i386, Windows-x86_64 ... """
        return "%s-%s" % (self._ostype, self._machine)
    # OS extraction

    def OSRelease(self):
        release_info = {}
        with open("/etc/os-release") as f:
            for line in f:
                k, v = line.rstrip().split("=")
                # .strip('"') will remove if there or else do nothing
                release_info[k] = v.strip('"')

        return release_info

    def OSFlavour(self, teststring=None):
        if not self._osflavor or teststring:
            if self._ostype == "Windows":
                self._osflavor = self._sysinfo[2]
                self._osversion = self._sysinfo[3]
            elif self._ostype == "SunOS":
                self._osflavor = "sun"
                self._osversion = "4.x"
            elif self._ostype == "Darwin":
                ver_list = [int(v) for v in self._sysinfo[2].split('.')]
                if len(ver_list) > 2:
                    os_maj_release = ver_list[0] - 4
                    os_min_release = ver_list[1]
                    if os_maj_release == 3:
                        self._osflavor = 'Panther'
                    elif os_maj_release == 4:
                        self._osflavor = 'Tiger'
                    elif os_maj_release == 5:
                        self._osflavor = 'Leopard'
                    elif os_maj_release == 6:
                        self._osflavor = 'Snow Leopard'
                    self._osversion = "10.%d.%d" % (os_maj_release, os_min_release)

            elif self._ostype == "Linux":
                for f in LINUX_RELEASE_FILES:
                    if os.path.exists(f):
                        cont = " ".join(open(f).readlines())
                        break
                if teststring:
                    cont = teststring
                found = False
                for f in LINUX_FLAVOUR_ALIASES:
                    if not found:
                        for s in LINUX_FLAVOUR_ALIASES[f]:
                            if not found:
                                if cont.upper().find(s.upper()) != -1:
                                    self._osflavor = LINUX_FLAVOUR_ALIASES[f][0]
                                    found = True
                                    break
                            else:
                                break
                    else:
                        break
                vmatch = re.compile(r"\ +(\d+(?:\.\d+)*)")
                m = vmatch.search(cont)
                if m:
                    self._osversion = m.group(1)

        return self._osflavor

    def OSVersion(self, position=None, teststring=None):
        """
        returns version of the OS up to position
        @param position: last position of version (no included)
        @param teststring: test entry
        """
        if not self._osversion:
            if self._ostype == "Windows":
                self._osversion = self._sysinfo[3]
            elif self._ostype == "SunOS":
                self._osversion = "4.x"
            elif self._ostype == "Darwin":
                ver_list = [int(v) for v in self._sysinfo[2].split(".")]
                if len(ver_list) > 2:
                    os_maj_release = ver_list[0] - 4
                    os_min_release = ver_list[1]
                    self._osversion = "10.%d.%d" % (os_maj_release, os_min_release)
            elif self._ostype == "Linux":
                for f in LINUX_RELEASE_FILES:
                    if os.path.exists(f):
                        cont = " ".join(open(f).readlines())
                        break
                if teststring:
                    cont = teststring
                vmatch = re.compile(r"\ +(\d+(?:\.\d+)*)")
                m = vmatch.search(cont)
                if m:
                    self._osversion = m.group(1)
                else:
                    self._osversion = ""

        osver = self._osversion

        # returns at most the number of position specified.
        if position and self._osversion:
            osver = ".".join(self._osversion.split(".")[:position])

        return osver

    def _findCompiler(self, compiler_exe):

        return [c for c in
                [os.path.join(d, compiler_exe)
                 for d in os.environ["PATH"].split(os.pathsep)
                 if d.startswith('/usr')]
                if os.path.exists(c)][0]

    def nativeCompilerName(self):
        c_name = "gcc"
        if self._ostype == "Windows":
            c_name = "vc"
        else:
            if self._ostype == "Darwin":
                if tuple([int(v) for v in self.OSVersion().split(".")]) >= (10, 9):
                    c_name = "clang"
                    cpp_name = "clang++"
                    gpp = self._findCompiler(cpp_name)
                    compstr = " ".join(
                        os.popen3(gpp + " --version")[1].readlines()).strip()
                    m = re.search(r"\([^)]*LLVM *(\d+\.?\d*)", compstr)
                    if not m:
                        # if the related genuine clang compiler cannot be found
                        # assume this is an unrelated Apple LLVM compiler
                        c_name = "llvm"
        return c_name

    def nativeCompilerVersionFromName(self, compiler_name, position=None):
        version = "0.0.0"
        ncv = version

        compiler_root = {"gcc": "g++", "clang": "clang++", "llvm": "clang++"}

        compiler_re = dict()
        compiler_re["gcc"] = re.compile(b"\ +(\d+(?:\.\d+)*)")
        compiler_re["clang"] = re.compile(b"\([^)]*LLVM *(\d+\.?\d*)")
        compiler_re["llvm"] = re.compile(b"\ +(\d+(?:\.\d+)*)")

        if compiler_name == "vc":
            ncv = "9.0.0"
        else:
            try:
                gpp = self._findCompiler(compiler_root[compiler_name])
                compstr = Popen(gpp + " --version", shell=True,
                                stdin=PIPE, stdout=PIPE, stderr=PIPE,
                                close_fds=True).communicate()[0]
                m = compiler_re[compiler_name].search(compstr)

                if m:
                    ncv = m.group(1).decode()
                else:
                    ncv = None
            except:
                ncv = None

        if position:
            try:
                ncv = ".".join(version.split(".")[:position])
            except AttributeError:
                ncv = None
        return ncv

    def nativeCompilerVersion(self, position=None):
        """
        return the native compiler version
        @param position: if not None returns up to the nth position. ie for gcc 3.4.5 with
        position=2, it returns 3.4
        """
        if not self._compversion:

            nc_name = self.nativeCompilerName()

            self._compversion = self.nativeCompilerVersionFromName(
                nc_name)

        ncv = self._compversion

        if position:
            try:
                ncv = ".".join(self._compversion.split(".")[:position])
            except AttributeError:
                ncv = None
        return ncv

    def nativeCompiler(self):

        if not self._compiler:

            root_name = self.nativeCompilerName()
            try:
                cvers = [
                    int(c) for c in self.nativeCompilerVersion(position=2).split(".")]
                self._compiler = "%s%d%d" % (root_name, cvers[0], cvers[1])
            except:
                self._compiler = None

        return self._compiler
    # CMT derived informations

    def architecture(self):
        """ returns the CMT architecture """
        arch = "ia32"
        if re.compile(r'i\d86').match(self.machine()):
            arch = "ia32"
        elif re.compile(r'x86_64').match(self.machine()):
            arch = "amd64"
        elif re.compile(r'ia64').match(self.machine()):
            arch = "ia64"
        elif re.compile(r'power mac', re.I).match(self.machine()):
            arch = "ppc"
        elif self.OSType() == "Windows":
            arch = sys.platform
        return arch

    def CMTSystem(self):
        """ returns the CMTBIn variable used by CMT itself """
        cmtsystem = None
        if self.OSType() == "Windows":
            cmtsystem = "VisualC"
        elif self.OSType() == "Darwin":
            cmtsystem = "Darwin-i386"
        else:
            if self.machine() in ARCH_RUNTIME_COMPATIBILITY["i586"]:
                cmtsystem = "%s-i386" % self.OSType()
            else:
                cmtsystem = "%s-%s" % (self.OSType(), self.machine())
        return cmtsystem

    def binaryOSFlavour(self):
        """ returns the CMT short name for the OS flavour and version """
        cmtflavour = None
        if self.OSType() == "Windows":
            cmtflavour = "win%s" % self.arch()
        elif self.OSType() == "SunOS":
            cmtflavour = self.OSFlavour() + \
                self.OSVersion(position=2).replace(".", "")
        elif self.OSType() == "Darwin":
            cmtflavour = "osx%s" % self.OSVersion(position=2).replace(".", "")
        elif self.OSType() == "Linux":
            for f in LINUX_FLAVOUR_ALIASES:
                if self.OSFlavour() == LINUX_FLAVOUR_ALIASES[f][0]:
                    cmtflavour = f + self.OSVersion(position=1)
                    if self.OSFlavour() in ("SuSE", "Redhat"):
                        cmtflavour = f + self.OSVersion(position=2)
                    if self.OSFlavour() == "SuSE" and int(self.OSVersion(position=1)) > 10:
                        cmtflavour = f + self.OSVersion(position=1)
                if not cmtflavour:
                    cmtflavour = "lx"
        return cmtflavour

    def OSEquivalentFlavour(self):
        """ returns the CMT short name for the OS compatible flavour and version """
        cmtflavour = None
        for f in FLAVOUR_RUNTIME_EQUIVALENCE:
            if self.binaryOSFlavour() in FLAVOUR_RUNTIME_EQUIVALENCE[f]:
                cmtflavour = f
                break
        return cmtflavour

    def compatibleBinaryTag(self, all_types=False):
        """ return the list of compatible binary tags """
        compatibles = []
        equiv = self.OSEquivalentFlavour()
        machine = self.machine()
        if equiv in FLAVOUR_RUNTIME_COMPATIBILITY:
            for f in FLAVOUR_RUNTIME_COMPATIBILITY[equiv]:
                for m in ARCH_RUNTIME_COMPATIBILITY[machine]:
                    allcomp = []
                    if f in SUPPORTED_COMPILERS:
                        allcomp.extend(SUPPORTED_COMPILERS[f])
                    # add the native compiler
                    nc = self.nativeCompiler()
                    if nc:
                        allcomp.append(nc)
                    for c in allcomp:
                        n = getBinaryTag(m, f, c)
                        if n not in compatibles:
                            compatibles.append(n)
                        if all_types:
                            for t in BUILD_TYPES:
                                n = getBinaryTag(m, f, c, t)
                                if n not in compatibles:
                                    compatibles.append(n)

        return compatibles

    def supportedBinaryTag(self, all_types=False):
        """
        returns the list of supported binary tags among the compatible ones. This
        means the ones which are shipped and usable on a local site.
        @param all_types: if True returns also the debug configs. Otherwise only the opt ones.
        """
        compatibles = self.compatibleBinaryTag(all_types)
        supported = []
        binary_set = set(BINARY_LIST)
        for c in compatibles:
            if c in binary_set and c not in supported:
                supported.append(c)
        return supported

    def nativeBinaryTag(self, binary_type=DEFAULT_BUILD_TYPE):
        """
        Returns the native configuration if possible. Guess also the compiler
        on linux platforms
        @param all_types: if True returns also the debug configs. Otherwise only the opt ones.
        """
        comp = self.nativeCompiler()
        mach = self.machine()
        osflav = self.binaryOSFlavour()
        natconf = getBinaryTag(architecture=mach, platformtype=osflav,
                               compiler=comp, binary_type=binary_type)
        return natconf

    def DiracPlatform(self):
        """
        return Dirac-style platform
        """
        platformlist = [platform.system(), platform.machine()]
        if self.OSType() == "Linux":
            # get version of highest libc installed
            if self.arch() == "64":
                lib = '/lib64'
            else:
                lib = '/lib'
            libs = []
            for l in os.listdir(lib):
                if l.find('libc-') == 0 or l.find('libc.so') == 0:
                    libs.append(os.path.join(lib, l))
            libs.sort()
            platformlist.append('-'.join(platform.libc_ver(libs[-1])))
        elif self.OSType() == "Darwin":
            platformlist.append('.'.join(platform.mac_ver()[0].split(".")[:2]))
        elif self.OSType() == "Windows":
            platformlist.append(platform.win32_ver()[0])
        else:
            platformlist.append(platform.release())

        platformstr = "_".join(platformlist)
        return platformstr

    def numberOfCPUs(self):
        """ Number of virtual or physical CPUs on this system, i.e.
        user/real as output by time(1) when called with an optimally scaling userspace-only program"""
        res = 1
        # Python 2.6+
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass

        # POSIX
        try:
            res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

            if res > 0:
                return res
        except (AttributeError, ValueError):
            pass

        # Windows
        try:
            res = int(os.environ['NUMBER_OF_PROCESSORS'])

            if res > 0:
                return res
        except (KeyError, ValueError):
            pass
        # BSD
        try:
            sysctl = Popen(
                ['sysctl', '-n', 'hw.ncpu'], stdout=PIPE)
            scStdout = sysctl.communicate()[0]
            res = int(scStdout)

            if res > 0:
                return res
        except (OSError, ValueError, ImportError):
            pass

        # Linux
        try:
            res = open('/proc/cpuinfo').read().count('processor\t:')

            if res > 0:
                return res
        except IOError:
            pass

        # Solaris
        try:
            pseudo_devices = os.listdir('/devices/pseudo/')
            expr = re.compile('^cpuid@[0-9]+$')

            res = 0
            for pd in pseudo_devices:
                if expr.match(pd) != None:
                    res += 1

            if res > 0:
                return res
        except OSError:
            pass

        # Other UNIXes (heuristic)
        try:
            try:
                dmesg = open('/var/run/dmesg.boot').read()
            except IOError:
                dmesg_process = Popen(
                    ['dmesg'], stdout=PIPE)
                dmesg = dmesg_process.communicate()[0]

            res = 0
            while '\ncpu' + str(res) + ':' in dmesg:
                res += 1

            if res > 0:
                return res
        except OSError:
            pass

        return res

    def LSBDistributorID(self):
        """
        wrapper around lsb_release -i
        """
        if not self._lsb_distributor_id and self.OSType() == "Linux":
            if hasCommand("lsb_release"):
                lsbstr = os.popen("lsb_release -i").read()[:-1]
                if lsbstr:
                    self._lsb_distributor_id = lsbstr.split(":")[-1].strip()
        return self._lsb_distributor_id

    def LSBDescription(self):
        """
        wrapper around lsb_release -d
        """
        if not self._lsb_description and self.OSType() == "Linux":
            if hasCommand("lsb_release"):
                lsbstr = os.popen("lsb_release -d").read()[:-1]
                if lsbstr:
                    self._lsb_description = lsbstr.split(":")[-1].strip()
        return self._lsb_description

    def LSBRelease(self):
        """
        wrapper around lsb_release -r
        """
        if not self._lsb_release and self.OSType() == "Linux":
            if hasCommand("lsb_release"):
                lsbstr = os.popen("lsb_release -r").read()[:-1]
                if lsbstr:
                    self._lsb_release = lsbstr.split(":")[-1].strip()
        return self._lsb_release

    def LSBCodeName(self):
        """
        wrapper around lsb_release -c
        """
        if not self._lsb_codename and self.OSType() == "Linux":
            if hasCommand("lsb_release"):
                lsbstr = os.popen("lsb_release -c").read()[:-1]
                if lsbstr:
                    self._lsb_codename = lsbstr.split(":")[-1].strip()
        return self._lsb_codename
