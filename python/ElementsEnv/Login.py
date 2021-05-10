""" Main script to setup the basic ElementsEnv environment """

import sys
import os
import logging
import shutil

#============================================================================
# setting up the core environment for Python only. This has to be done before
# the import of the local modules.
# In principle, only the PYTHONPATH (internal) setup is needed. The PATH and
# other are delayed to the created setup script

# first try to use the installed prefix path
MY_OWN_PREFIX = "%(this_install_prefix)s"
HAS_PREFIX = False

if os.path.exists(MY_OWN_PREFIX):
    HAS_PREFIX = True

MY_OWN_VERSION = "%(this_install_version)s"
HAS_VERSION = False

if not MY_OWN_VERSION.startswith("%"):
    HAS_VERSION = True

if HAS_PREFIX:
    from distutils.sysconfig import get_python_lib
    if MY_OWN_PREFIX != "/usr":
        # funky location yeah
        PYTHON_LOC = get_python_lib(prefix=MY_OWN_PREFIX)
    else:
        # if the location is standard, don't try to be funny
        PYTHON_LOC = None
else:
    # use the local properties if the intall_path is no available
    try:
        _THIS_FILE = __file__
    except NameError:
        # special procedure to handle the situation when __file__ is not defined.
        # It happens typically when trying to use pdb.
        from imp import find_module, load_module
        _FF, _FILENAME, _DESC = find_module("ElementsEnv")
        try:
            LBCONF_PACKAGE = load_module('ElementsEnv', _FF, _FILENAME, _DESC)
            _FF, _FILENAME, _DESC = find_module(
                'Login', LBCONF_PACKAGE.__path__)
            _THIS_FILE = _FILENAME
        finally:
            _FF.close()
    # Bootstrapping the python location
    _PYEUC_DIR = os.path.dirname(_THIS_FILE)
    _PY_DIR = os.path.dirname(_PYEUC_DIR)
    if os.path.basename(_PYEUC_DIR) == "ElementsEnv":
        _BASE_DIR = os.path.dirname(_PY_DIR)
        PYTHON_LOC = _PY_DIR

if PYTHON_LOC:
    sys.path.insert(0, PYTHON_LOC)

#============================================================================

from Euclid.Platform import getBinaryOfType, BUILD_TYPES, DEFAULT_BUILD_TYPE
from Euclid.Platform import getBinaryTypeName
from Euclid.Platform import getCompiler, getPlatformType, getArchitecture
from Euclid.Platform import isBinaryType, NativeMachine
from Euclid.Script import SourceScript
from Euclid.Path import pathPrepend, getClosestPath

__version__ = ""

if HAS_VERSION:
    __version__ = MY_OWN_VERSION

#-------------------------------------------------------------------------
# Helper functions


def getLoginEnv(optionlist=None):
    if not optionlist:
        optionlist = []
    s = LoginScript()
    s.parseOpts(optionlist)
    return s.setEnv()


def getLoginAliases(optionlist=None):
    if not optionlist:
        optionlist = []
    s = LoginScript()
    s.parseOpts(optionlist)
    return s.setAliases()


def getLoginExtra(optionlist=None):
    if not optionlist:
        optionlist = []
    s = LoginScript()
    s.parseOpts(optionlist)
    return s.setExtra()

#-------------------------------------------------------------------------


class LoginScript(SourceScript):
    _version = __version__
    _description = __doc__
    _description += """

The type is to be chosen among the following list:
%s and the default is %s.
""" % (", ".join(BUILD_TYPES.keys()), DEFAULT_BUILD_TYPE)

    def __init__(self, usage=None, version=None):
        self._nativemachine = NativeMachine()
        SourceScript.__init__(self, usage, version)
        self.platform = ""
        self.binary = ""
        self.compdef = ""
        self._target_binary_type = None
        self._tried_local_setup = False
        self._tried_afs_setup = False

#-------------------------------------------------------------------------
# Option definition

    def defineOpts(self):
        """ define commandline options """
        parser = self.parser
        parser.set_defaults(binary_tag=None)
        parser.add_option("-b", "--binary-tag",
                          dest="binary_tag",
                          help="set BINARY_TAG.",
                          fallback_env="BINARY_TAG")
        parser.set_defaults(userarea=None)
        parser.add_option("-u", "--userarea",
                          dest="userarea",
                          help="set User_area.",
                          fallback_env="User_area")
        parser.set_defaults(remove_userarea=False)
        parser.add_option("--no-userarea",
                          dest="remove_userarea",
                          action="store_true",
                          help="prevent the addition of a user area [default: %default]")
        parser.set_defaults(sharedarea=None)
        parser.add_option("-s", "--shared",
                          dest="sharedarea",
                          help="set the shared area",
                          fallback_env="EUCLID_BASE")
        parser.set_defaults(strip_path=True)
        parser.add_option("--no-strip-path",
                          dest="strip_path",
                          action="store_false",
                          help="prevent the cleanup of invalid entries in pathes")
        parser.add_option("--strip-path",
                          dest="strip_path",
                          action="store_true",
                          help="activate the cleanup of invalid entries in pathes [default: %default]")
        parser.set_defaults(no_explicit_python_version=False)
        parser.add_option("--no-explicit-python-version",
                          dest="no_explicit_python_version",
                          action="store_true",
                          help="inhibits the setup of variable for an explicit python version")
# specific native platform options
        if self._nativemachine.OSType() == "Darwin":
            parser.add_option("--macport-location",
                              dest="macport_location",
                              help="Set the MacOSX port install base",
                              fallback_env="MACPORT_LOCATION")
            parser.set_defaults(use_macport=True)
            parser.add_option("--no-macport",
                              dest="use_macport",
                              action="store_false",
                              help="prevent the setup of the Mac Port location")

#-------------------------------------------------------------------------

    def _checkEnvVar(self, envvar):

        ev = self.Environment()
        log = logging.getLogger()

        if envvar in ev:
            log.debug("%s is set to %s" % (envvar, ev[envvar]))
            if not ev[envvar].endswith(os.pathsep):
                log.warn("The %s variable doesn't end with a \"%s\""
                          % (envvar, os.pathsep))

#-------------------------------------------------------------------------
    def setOwnPath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()

        if "PYTHONPATH" in ev:
            log.debug("%s is set to %s" % ("PYTHONPATH", ev["PYTHONPATH"]))

        bin_loc = None

        if PYTHON_LOC:
            bin_loc = getClosestPath(
                PYTHON_LOC, os.sep.join(["bin", "ELogin.sh"]), alloccurences=False)
            if not bin_loc:
                bin_loc = getClosestPath(
                    PYTHON_LOC, os.sep.join(["scripts", "ELogin.sh"]), alloccurences=False)

        if bin_loc:
            the_loc = os.path.dirname(bin_loc[0])
            ev["PATH"] = pathPrepend(ev["PATH"],
                                     the_loc,
                                     exist_check=opts.strip_path,
                                     unique=opts.strip_path)

        log.debug("%s is set to %s" % ("PATH", ev["PATH"]))

        # try the installed directory in $prefix/share/ElementsEnv/cmake/...

        if PYTHON_LOC:
            python_prefix = PYTHON_LOC
        else:
            python_prefix = "/usr"

        cmake_loc = getClosestPath(python_prefix,
                                   os.sep.join(
                                       ["share", "ElementsEnv", "cmake", "ElementsProjectConfig.cmake"]),
                                   alloccurences=False)
        if not cmake_loc:
            # use the local source directory
            cmake_loc = getClosestPath(python_prefix,
                                       os.sep.join(
                                           ["data", "cmake", "ElementsProjectConfig.cmake"]),
                                       alloccurences=False)

        if cmake_loc:
            the_loc = os.path.dirname(cmake_loc[0])
            if "CMAKE_PREFIX_PATH" in ev:
                ev["CMAKE_PREFIX_PATH"] = pathPrepend(ev["CMAKE_PREFIX_PATH"],
                                                      the_loc,
                                                      exist_check=opts.strip_path,
                                                      unique=opts.strip_path)
            elif os.path.exists(the_loc):
                ev["CMAKE_PREFIX_PATH"] = the_loc

        if "CMAKE_PREFIX_PATH" in ev:
            log.debug("%s is set to %s" % ("CMAKE_PREFIX_PATH", ev["CMAKE_PREFIX_PATH"]))

#-------------------------------------------------------------------------

    def fixPath(self):

        ev = self.Environment()
        log = logging.getLogger()

        var_list = ["MANPATH", "TEXINPUTS"]

        for v in var_list:
            if v in ev:
                if not ev[v].endswith(os.pathsep):
                    log.debug("Adding \"%s\" to the %s variable" % (os.pathsep, v))
                    ev[v] += os.pathsep

        for v in var_list:
            self._checkEnvVar(v)

#-------------------------------------------------------------------------

    def setPath(self):
        ev = self.Environment()
        al = self.Aliases()
        opts = self.options
        log = logging.getLogger()
        if not opts.strip_path:
            log.debug("Disabling the path stripping")
            ev["E_NO_STRIP_PATH"] = "1"
        else:
            if "E_NO_STRIP_PATH" in ev:
                log.debug("Reenabling the path stripping")
                del ev["E_NO_STRIP_PATH"]

        self.setOwnPath()

        if self._nativemachine.OSType() == "Darwin":
            if ("MACPORT_LOCATION" not in ev) and os.path.exists("/opt/local"):
                ev["MACPORT_LOCATION"] = "/opt/local"

            if "MACPORT_LOCATION" in ev:
                log.debug("%s is set to %s" % ("MACPORT_LOCATION", ev["MACPORT_LOCATION"]))
                mac_bin = os.path.join(ev["MACPORT_LOCATION"], "bin")

                if "PATH" in ev:
                    ev["PATH"] = pathPrepend(ev["PATH"],
                                             mac_bin,
                                             exist_check=opts.strip_path,
                                             unique=opts.strip_path)
                elif os.path.exists(mac_bin):
                    ev["PATH"] = mac_bin

                al["make"] = "gmake"

                mac_man = os.path.join(ev["MACPORT_LOCATION"], "man")
                if "MANPATH" in ev:
                    ev["MANPATH"] = pathPrepend(ev["MANPATH"],
                                                mac_man,
                                                exist_check=opts.strip_path,
                                                unique=opts.strip_path)
                elif os.path.exists(mac_man):
                    ev["MANPATH"] = mac_man

        self.fixPath()

#-------------------------------------------------------------------------

    def setHomeDir(self):
        ev = self.Environment()
        log = logging.getLogger()
        if sys.platform == "win32" and "HOME" not in ev:
            ev["HOME"] = os.path.join(ev["HOMEDRIVE"], ev["HOMEPATH"])
            log.debug("Setting HOME to %s" % ev["HOME"])
        if sys.platform != "win32":
            user_var = "USER"
        else:
            user_var = "USERNAME"
        username = ev.get(user_var, None)
        if username:
            log.debug("User name is %s" % username)

        if sys.platform != "win32" and self.targetShell() == "sh" and "HOME" in ev:
            hprof = os.path.join(ev["HOME"], ".bash_profile")
            sprof = os.path.join("/etc", "skel", ".bash_profile")
            hlist = []
            hlist.append(hprof)
            hlist.append(os.path.join(ev["HOME"], ".bash_login"))
            hlist.append(os.path.join(ev["HOME"], ".profile"))
            if not [x for x in hlist if os.path.exists(x)]:
                if os.path.exists(sprof):
                    try:
                        shutil.copy(sprof, hprof)
                        log.warning("Copying %s to %s" % (sprof, hprof))
                    except IOError:
                        log.warning("Failed to copy %s to %s" % (sprof, hprof))
            hbrc = os.path.join(ev["HOME"], ".bashrc")
            sbrc = os.path.join("/etc", "skel", ".bashrc")
            if not os.path.exists(hbrc):
                if os.path.exists(sbrc):
                    try:
                        shutil.copy(sbrc, hbrc)
                        log.warning("Copying %s to %s" % (sbrc, hbrc))
                    except IOError:
                        log.warning("Failed to copy %s to %s" % (sbrc, hbrc))
        if "LD_LIBRARY_PATH" not in ev:
            ev["LD_LIBRARY_PATH"] = ""
            log.debug("Setting a default LD_LIBRARY_PATH")

        if "ROOTSYS" not in ev:
            ev["ROOTSYS"] = ""
            log.debug("Setting a default ROOTSYS")

        self.setUserArea()

    def setUserArea(self):
        log = logging.getLogger()
        opts = self.options
        ev = self.Environment()
        if not opts.remove_userarea:
            newdir = False
            if not opts.userarea:
                # @todo: use something different for window
                opts.userarea = os.path.join(ev["HOME"], "Work", "Projects")
            ev["User_area"] = opts.userarea
            log.debug("User_area is set to %s" % ev["User_area"])

            rename_cmakeuser = False
            # is a file, a directory or a valid link
            if os.path.exists(opts.userarea):
                # is a file or a link pointing to a file
                if os.path.isfile(opts.userarea):
                    log.warning("%s is a file" % opts.userarea)
                    rename_cmakeuser = True
                    newdir = True
                # is a directory or a link pointing to a directory. Nothing to
                # do
                else:
                    log.debug("%s is a directory" % opts.userarea)
            else:  # doesn't exist or is an invalid link
                if os.path.islink(opts.userarea):  # broken link
                    log.warning("%s is a broken link" % opts.userarea)
                    rename_cmakeuser = True
                newdir = True
            if rename_cmakeuser:
                bak_userarea = opts.userarea + "_bak"
                if not os.path.exists(bak_userarea):
                    if os.path.islink(bak_userarea):
                        try:
                            os.remove(bak_userarea)  # remove broken link
                        except IOError:
                            log.warning("Can't remove %s" % bak_userarea)
                    try:
                        os.rename(opts.userarea, opts.userarea + "_bak")
                        log.warning("Renamed %s into %s" % (opts.userarea, opts.userarea + "_bak"))
                    except IOError:
                        log.warning("Can't rename %s into %s" % (opts.userarea, opts.userarea + "_bak"))
                else:
                    log.warning("Can't backup %s because %s is in the way" % (opts.userarea, bak_userarea))
                    log.warning("No %s directory created" % opts.userarea)
                    newdir = False
            if newdir:
                try:
                    os.makedirs(opts.userarea)
                    self.addEcho(
                        " --- a new User_area directory has been created in your HOME directory")
                except (IOError, OSError):
                    log.warning("Can't create %s" % opts.userarea)
        elif "User_area" in ev:
            del ev["User_area"]
            log.debug("Removed User_area from the environment")

    def getSupportedBinaryTag(self):
        """
        returns the best matched BINARY_TAG for the wilcard string
        """
        theconf = None
        log = logging.getLogger()

        if self._target_binary_type:
            log.debug("Guessing BINARY_TAG for the %s type" % self._target_binary_type)
            supported_configs = self._nativemachine.supportedBinaryTag(
                all_types=True)
            supported_configs = [
                s for s in supported_configs if isBinaryType(s, self._target_binary_type)]
        else:
            log.debug("Guessing BINARY_TAG")
            supported_configs = self._nativemachine.supportedBinaryTag()

        if supported_configs:
            theconf = supported_configs[0]

        return theconf

    def setBinaryTag(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()
        self.binary = None
        self.platform = None
        self.compdef = None

        if opts.binary_tag:
            # the binary has either beeen passed with the -b option or
            # with the BINARY_TAG env variable
            log.debug("Using the provided BINARY_TAG %s" % opts.binary_tag)
            theconf = opts.binary_tag
        else:
            # the type is completely guessed
            theconf = self.getSupportedBinaryTag()
            if not theconf:
                log.debug("Falling back on the native BINARY_TAG")
                theconf = self._nativemachine.nativeBinaryTag()

        if theconf:
            if self._target_binary_type:
                log.debug("Reusing %s BINARY_TAG to set it to %s mode" % (theconf, self._target_binary_type))
                theconf = getBinaryOfType(theconf, self._target_binary_type)
                log.debug("BINARY_TAG set to %s" % theconf)
            else:
                self._target_binary_type = getBinaryTypeName(theconf)
            self.binary = getArchitecture(theconf)
            self.platform = getPlatformType(theconf)
            self.compdef = getCompiler(theconf)
            opts.binary_tag = theconf
        else:
            log.error("Cannot set the BINARY_TAG environment variable")

        supported_binarytags = self._nativemachine.supportedBinaryTag(
            all_types=True)
        if opts.binary_tag not in supported_binarytags:
            log.warning("%s is not in the list of distributed configurations" % opts.binary_tag)
            if supported_binarytags:
                log.warning(
                    "Please switch to a supported one with 'ELogin -b <binary_tag>' before building")
                log.warning("Supported binary tags: %s" % ", ".join(supported_binarytags))

        if sys.platform == "win32":
            ev["BINARY_TAG"] = getBinaryOfType(theconf, "Debug")
        else:
            ev["BINARY_TAG"] = opts.binary_tag

        log.debug("BINARY_TAG is set to %s" % ev["BINARY_TAG"])

    def setSGShostos(self):
        '''
        Set the environment variable SGS_hostos, used by the 'sgs-' compiler wrappers.
        '''
        ev = self.Environment()
        nm = self._nativemachine
        # we take only the first two elements of the native BINARY_TAG, e.g.
        #  x86_64-slc5-gcc46-opt -> x86_64-slc5
        ev['SGS_hostos'] = '-'.join(nm.nativeBinaryTag().split('-')[:2])

    def setCMakePath(self):
        ev = self.Environment()
        opts = self.options
        log = logging.getLogger()

        self.setHomeDir()

        prefix_path = []

        if not opts.remove_userarea and "User_area" in ev:
            prefix_path.append(ev["User_area"])

        if opts.sharedarea:
            ev["EUCLIDPROJECTPATH"] = opts.sharedarea

        if "EUCLIDPROJECTPATH" not in ev:
            if "EUCLID_BASE" in ev:
                ev["EUCLIDPROJECTPATH"] = ev["EUCLID_BASE"]

        if "EUCLIDPROJECTPATH" not in ev:
            if os.path.exists("%(this_euclid_base)s"):
                ev["EUCLIDPROJECTPATH"] = "%(this_euclid_base)s"

        if "EUCLIDPROJECTPATH" in ev:
            log.debug("The value of EUCLIDPROJECTPATH is %s" % ev["EUCLIDPROJECTPATH"])
            prefix_path.append(ev["EUCLIDPROJECTPATH"])

        if not opts.remove_userarea and "User_area" in ev:
            prefix_path.append(ev["User_area"])

        if "CMAKE_PROJECT_PATH" not in ev:
            ev["CMAKE_PROJECT_PATH"] = ""

        for p in prefix_path:
            if not os.path.exists(p):
                log.warn("The %s directory doesn't exist." % p)
            ev["CMAKE_PROJECT_PATH"] = pathPrepend(ev["CMAKE_PROJECT_PATH"],
                                                   p,
                                                   exist_check=False,
                                                   unique=opts.strip_path)

        log.debug("The value of CMAKE_PROJECT_PATH is %s" % ev["CMAKE_PROJECT_PATH"])

        log.debug("CMAKE_PROJECT_PATH is set to %s" % ev["CMAKE_PROJECT_PATH"])

        if not opts.no_explicit_python_version:

            # get the explicit python version used to call this script

            __full_exec__ = sys.executable
            __exec__ = os.path.basename(__full_exec__)
            __exec_maj_vers = "%d" % sys.version_info[0]
            __exec_exp_vers = ""

            if __exec__.endswith(__exec_maj_vers):
                __exec_exp_vers = __exec_maj_vers

            if __exec_exp_vers:
                log.debug("Using python explicit version: %s" % __exec_exp_vers)
                if "CMAKEFLAGS" in ev:
                    ev["CMAKEFLAGS"] += " -DPYTHON_EXPLICIT_VERSION=%s" % __exec_exp_vers
                else:
                    ev["CMAKEFLAGS"] = "-DPYTHON_EXPLICIT_VERSION=%s" % __exec_exp_vers

        if "MACPORT_LOCATION" in ev:
            if "CMAKEFLAGS" in ev:
                ev["CMAKEFLAGS"] += " -DCMAKE_FIND_FRAMEWORK=LAST"
                ev["CMAKEFLAGS"] += " -DCMAKE_FIND_ROOT_PATH=%s" % ev["MACPORT_LOCATION"]
            else:
                ev["CMAKEFLAGS"] = "-DCMAKE_FIND_FRAMEWORK=LAST"
                ev["CMAKEFLAGS"] += " -DCMAKE_FIND_ROOT_PATH=%s" % ev["MACPORT_LOCATION"]

    def setExtraEnv(self):

        ev = self.Environment()
        ev["ELEMENTS_NAMING_DB_URL"] = "https://pieclddj00.isdc.unige.ch/elementsnaming"
        ev["CTEST_OUTPUT_ON_FAILURE"] = "1"

    def copyEnv(self):
        ev = self.Environment()
        retenv = dict(ev.env)
        al = self.Aliases()
        retaliases = dict(al.env)
        retextra = self.extra()
        return retenv, retaliases, retextra

    def setEnv(self):
        log = logging.getLogger()
        log.debug("Entering the environment setup")
        self.setPath()

        self.setBinaryTag()
        self.setCMakePath()
        self.setExtraEnv()

        # this is use internally by the 'sgs-' compiler wrapper.
        self.setSGShostos()

        # return a copy otherwise the environment gets restored
        # at the destruction of the instance

        return self.copyEnv()[0]

    def setAliases(self):
        al = self.Aliases()
        if self.targetShell() == "sh":
            al["ELogin"] = ". \\`/usr/bin/which  ELogin.%s\\`" % self.targetShell()
        else:
            al["ELogin"] = "source \\`/usr/bin/which ELogin.%s\\`" % self.targetShell()

        al["ERun"] = "E-Run"
        al["EuclidRun"] = "E-Run"

        return self.copyEnv()[1]

    def setExtra(self):
        return self.copyEnv()[2]

    def manifest(self, binary_type=DEFAULT_BUILD_TYPE):
        ev = self.Environment()
        opts = self.options
        if opts.log_level != "CRITICAL":
            self.addEcho("*" * 80)
            vers = __version__
            if vers:
                self.addEcho(
                    "*" + ("---- ElementsEnv Login %s ----" % vers).center(78) + "*")
            else:
                self.addEcho(
                    "*" + "---- ElementsEnv Login ----".center(78) + "*")
            if self.binary:
                self.addEcho("*" + ("Building with %s on %s %s system (%s)" % (
                    self.compdef, self.platform, self.binary, ev["BINARY_TAG"])).center(78) + "*")
            else:  # for windows
                self.addEcho("*" + ("Building with %s on %s system (%s)" %
                                    (self.compdef, self.platform, ev["BINARY_TAG"])).center(78) + "*")
            self.addEcho("*" * 80)
            if "User_area" in ev:
                self.addEcho(" --- User_area is set to %s" % ev["User_area"])
            if "EUCLIDPROJECTPATH" in ev:
                self.addEcho(" --- EUCLIDPROJECTPATH is set to:")
                for p in ev["EUCLIDPROJECTPATH"].split(os.pathsep):
                    if p:
                        self.addEcho("    %s" % p)
            if self._nativemachine.OSType() == "Darwin" and opts.use_macport:
                if "MACPORT_LOCATION" in ev:
                    self.addEcho(" --- Using MacPort location from %s" %
                                 ev["MACPORT_LOCATION"])
            self.addEcho("-" * 80)

    def parseOpts(self, args):
        SourceScript.parseOpts(self, args)
        for a in self.args:
            for b in BUILD_TYPES:
                if (a.lower() == b.lower()) or (a.lower() == BUILD_TYPES[b].lower()):
                    self._target_binary_type = b

    def main(self):
        opts = self.options

        log = logging.getLogger()

        if HAS_PREFIX:
            log.debug("The installation prefix is: %s" % MY_OWN_PREFIX)

        # first part: the environment variables
        if not opts.shell_only:
            self.setEnv()

        # second part the aliases
        self.setAliases()

        if not opts.shell_only:
            # the shell-only part has to be completely silent
            self.manifest()

        self.flush()

        return 0


if __name__ == '__main__':
    sys.exit(LoginScript(usage="%prog [options] [type]").run())
