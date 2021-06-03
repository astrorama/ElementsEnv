#!/usr/bin/env python
# Commit Id: $Format:%H$
# Author:    $Format:%an$
# Date  :    $Format:%ad$

try:
    from setuptools.command.install import install as _install
    from setuptools.command.sdist import sdist as _sdist
    from setuptools import Command
    from setuptools import setup
except:
    from distutils.command.install import install as _install
    from distutils.command.sdist import sdist as _sdist
    from distutils.core import Command
    from distutils.core import setup

from distutils.command.bdist_rpm import bdist_rpm as _bdist_rpm
from distutils.command.build import build as _build
from distutils.command.build_scripts import build_scripts as _build_scripts
from distutils.command.install_data import install_data as _install_data
from distutils.command.install_scripts import install_scripts as _install_scripts
from distutils.util import convert_path
from distutils import log

import os
import sys
import logging
from subprocess import call, check_output
from glob import glob
from stat import ST_MODE, S_IEXEC

logging.basicConfig(format='%(levelname)s\t: %(message)s', level=logging.INFO)

from string import Template

__version__ = "3.18.0"
__project__ = "ElementsEnv"
__full_exec__ = sys.executable
__usr_loc__ = os.path.dirname(os.path.dirname(__full_exec__))
__root_loc__ = os.path.dirname(__usr_loc__)
__exec__ = os.path.basename(__full_exec__)
__exec_maj_vers = "%d" % sys.version_info[0]
__exec_exp_vers = ""

if __exec__.endswith(__exec_maj_vers):
    __exec_exp_vers = __exec_maj_vers

# variable used for the package creation
dist_elementsenv_base = "/opt"
dist_etc_prefix = "/etc"
dist_usr_prefix = "/usr"
dist_custom_prefix = "/usr"
dist_exp_version = __exec_exp_vers
dist_impl_major_version = __exec_maj_vers
dist_full_exec_python = __full_exec__

this_use_custom_prefix = "no"

# Fix the dist locations if the python executable is not in the default location
if __usr_loc__ != "/usr":
    dist_elementsenv_base = os.path.join(__root_loc__, dist_elementsenv_base.lstrip("/"))
    dist_etc_prefix = os.path.join(__root_loc__, dist_etc_prefix.lstrip("/"))
    dist_usr_prefix = os.path.join(__root_loc__, dist_usr_prefix.lstrip("/"))
    dist_custom_prefix = os.path.join(__root_loc__, dist_custom_prefix.lstrip("/"))
    this_use_custom_prefix = "yes"

# variable interpolated at install time
this_elementsenv_base = "/opt"
this_custom_prefix = "/usr"

if not dist_exp_version:
    pytest_cmd = "py.test"
else:
    pytest_cmd = "py.test-%s" % dist_exp_version


def get_data_files(input_dir, output_dir):
    result = []
    for root, dirs, files in os.walk(input_dir):
        da_files = []
        for f in files:
            da_files.append(os.path.join(root, f))
        result.append(
            (os.sep.join([output_dir] + root.split(os.sep)[1:]), da_files))
    return result


these_files = get_data_files("data/cmake", __project__)
these_files += get_data_files("data/texmf", __project__)
these_files += get_data_files("data/make", __project__)


def get_script_files():
    result = []
    for root, dirs, files in os.walk("scripts"):
        for f in files:
            result.append(f)
    return result


# Please note the that the local install is
# also needed for --prefix. Take as example the
# /usr/local prefix.
use_local_install = False
for a in sys.argv:
    for b in ["--user", "--prefix", "--home"]:
        if a.startswith(b):
            use_local_install = True
    # subcase when the prefix is /usr
    if a.startswith("--prefix"):
        u_base = a.split("=")[1:][0]
        if u_base == "/usr":
            use_local_install = False

etc_install_root = None
install_root = None
for a in sys.argv:
    if a.startswith("--etc-root"):
        # TODO implement the extraction of the value from
        # the option
        e_base = a.split("=")[1:]
        if len(e_base) == 1:
            etc_install_root = e_base[0]
        sys.argv.remove(a)
    if a.startswith("--root"):
        # TODO implement the extraction of the value from
        # the option
        r_base = a.split("=")[1:]
        if len(r_base) == 1:
            install_root = r_base[0]

if not etc_install_root:
    if use_local_install:
        etc_install_prefix = "../etc"
    else:
        etc_install_prefix = "../../etc"
else:
    etc_install_prefix = os.path.join(etc_install_root, "etc")

etc_files = [(os.path.join(etc_install_prefix, "profile.d"), [os.path.join("data", "profile", "elementsenv.sh"),
                                       os.path.join("data", "profile", "elementsenv.csh")]),
             (os.path.join(etc_install_prefix, "sysconfig"),
                  [os.path.join("data", "sys", "config", "elementsenv")])
            ]

use_custom_install_root = False
for a in sys.argv:
    if a.startswith("--root"):
        # use custom install root. Possibly creating a
        # RPM. This will prevent the post install treatment.
        use_custom_install_root = True

skip_install_fix = False

# disable the postinstall script if needed. This is especially needed for the RPM
# creation. In that case the postinstall is done by the RPM spec file.
# This option is obsolete: rather use --skip-custom-postinstall
for a in sys.argv:
    if a.startswith("--skip-install-fix"):
        skip_install_fix = True
        sys.argv.remove(a)

skip_custom_postinstall = skip_install_fix
for a in sys.argv:
    if a.startswith("--skip-custom-postinstall"):
        skip_custom_postinstall = True
        sys.argv.remove(a)

for a in sys.argv:
    if a.startswith("--elementsenv-base"):
        # TODO implement the extratction of the value from
        # the option
        e_base = a.split("=")[1:]
        if len(e_base) == 1:
            this_elementsenv_base = e_base[0]
            this_custom_prefix = os.path.normpath(os.path.join(this_elementsenv_base, "..", "..", "usr"))
        sys.argv.remove(a)

for a in sys.argv:
    if a.startswith("--custom-prefix"):
        # TODO implement the extratction of the value from
        # the option
        c_base = a.split("=")[1:]
        if len(c_base) == 1:
            this_custom_prefix = c_base[0]
        sys.argv.remove(a)

fixscript_name = "FixInstallPath"


def getRMD160Digest(filepath):
    return check_output(["openssl", "dgst", "-rmd160", filepath]).split()[-1]


def getSHA256Digest(filepath):
    return check_output(["openssl", "dgst", "-sha256", filepath]).split()[-1]


class MyBuild(_build):

    def run(self):
        _build.run(self)


class MyBuildScripts(_build_scripts):

    def copy_scripts(self):
        # local fixscript. Before installation
        fixscript = os.path.join("scripts", fixscript_name)
        _build_scripts.copy_scripts(self)
        scripts_build_dir = self.build_dir
        for script in self.scripts:
            script = convert_path(script)
            outfile = os.path.join(self.build_dir, os.path.basename(script))
            call([__exec__, fixscript, "-n", "this_python_version", dist_impl_major_version, outfile])


class MySdist(_sdist):

    @staticmethod
    def _get_template_target(filename):
        fname, fext = os.path.splitext(os.path.basename(filename))
        if fext == ".in":
            return os.path.join("dist", fname)
        else:
            logging.error("Error: the %s file has not the '.in' extension" % filename)
            sys.exit(1)

    @staticmethod
    def _get_sdist_filepath():
        return os.path.join("dist", "%s-%s.tar.gz" % (__project__, __version__))

    @staticmethod
    def _get_changelog_filepath():
        return "ChangeLog"

    def expand_template_file(self, filename):
        out_fname = self._get_template_target(filename)
        logging.info("Generating %s from the %s template" % (out_fname, filename))
        rmd160_digest = getRMD160Digest(self._get_sdist_filepath())
        sha256_digest = getSHA256Digest(self._get_sdist_filepath())
        changelog_content = open(self._get_changelog_filepath()).read()
        with open(filename) as in_f:
            src = Template(in_f.read()).substitute(
                version=__version__,
                project=__project__,
                rmd160=rmd160_digest,
                sha256=sha256_digest,
                changelog=changelog_content,
                elementsenv_base=dist_elementsenv_base,
                usr_prefix=dist_usr_prefix,
                etc_prefix=dist_etc_prefix,
                custom_prefix=dist_custom_prefix,
                python_explicit_version=dist_exp_version,
                python_implicit_version=dist_impl_major_version,
                full_exec_python=dist_full_exec_python
                )
        with open(out_fname, "w") as out_f:
            out_f.write(src)

    def expand_templates(self):
        flist = []
        flist.append(os.path.join("data", "RPM", "%s.spec.in" % __project__))
        flist.append(os.path.join("data", "Ports", "Portfile.in"))
        for f in flist:
            if os.path.exists(f):
                self.expand_template_file(f)

    def run(self):
        _sdist.run(self)
        self.expand_templates()


class MyBdistRpm(_bdist_rpm):

    @staticmethod
    def run():
        logging.error("Cannot run directly the bdist_rpm target. Please rather use the generated " \
               "spec file (together with the sdist target) in the dist sub-directory")
        sys.exit(1)


class MyInstall(_install):

    def initialize_options(self):

        _install.initialize_options(self)

        parent_dir = os.path.dirname(os.path.abspath(__file__))

        dist_dir = os.path.join(parent_dir, "dist")

        if not os.path.exists(dist_dir):
            os.mkdir(dist_dir)

        self.record = os.path.join(dist_dir, "installed_files.txt")

    def get_login_scripts(self):
        p_list = []
        for c in ["ELogin", "ElementsEnv_group_login", "ElementsEnv_group_setup"]:
            for s in ["sh", "csh"]:
                file2fix = os.path.join(self.install_scripts, "%s.%s" % (c, s))
                if os.path.exists(file2fix):
                    p_list.append(file2fix)
        return p_list

    def get_profile_scripts(self):
        p_list = []
        this_install = self.get_etc_install_root()
        for s in ["sh", "csh"]:
            file2fix = os.path.join(
                this_install, "etc", "profile.d", "%s.%s" % ("elementsenv", s))
            if os.path.exists(file2fix):
                p_list.append(file2fix)
        return p_list

    def get_etc_install_root(self):
        if etc_install_root:
            this_install = etc_install_root
        else:
            if use_local_install:
                this_install = os.path.dirname(self.install_scripts)
            else:
                this_install = os.path.dirname(os.path.dirname(self.install_scripts))

        return this_install

    def fix_etc_install_path(self):
        fixscript = os.path.join(self.install_scripts, fixscript_name)
        proc_list = self.get_config_scripts()
        this_install = os.path.join(self.get_etc_install_root(), "etc")
        for p in proc_list:
            call([__exec__, fixscript, "-n", "this_etc_install_prefix", this_install, p])

    def fix_install_path(self):
        fixscript = os.path.join(self.install_scripts, fixscript_name)
        proc_list = self.get_login_scripts() + self.get_config_scripts()
        file2fix = os.path.join(self.install_lib, "ElementsEnv", "Login.py")
        if os.path.exists(file2fix):
            proc_list.append(file2fix)
        proc_list += self.get_profile_scripts()
        for p in proc_list:
            call([__exec__, fixscript, os.path.dirname(self.install_scripts), p])
        self.fix_etc_install_path()

    def fix_version(self):
        fixscript = os.path.join(self.install_scripts, fixscript_name)
        file2fix = os.path.join(self.install_lib, "ElementsEnv", "Login.py")
        if os.path.exists(file2fix):
            call(
                [__exec__, fixscript, "-n", "this_install_version", __version__, file2fix])

    def get_sysconfig_files(self):
        p_list = []

        this_install = self.get_etc_install_root()

        file2fix = os.path.join(this_install, "etc", "sysconfig", "elementsenv")
        if os.path.exists(file2fix):
            p_list.append(file2fix)
        return p_list

    def get_config_scripts(self):
        p_list = []
        for s in ["sh", "csh"]:
            file2fix = os.path.join(
                self.install_scripts, "%s.%s" % ("ElementsEnv_config", s))
            if os.path.exists(file2fix):
                p_list.append(file2fix)
        return p_list

    def fix_elementsenv_base(self):
        fixscript = os.path.join(self.install_scripts, fixscript_name)
        proc_list = self.get_sysconfig_files()
        proc_list += self.get_config_scripts()
        file2fix = os.path.join(self.install_lib, "ElementsEnv", "Login.py")
        if os.path.exists(file2fix):
            proc_list.append(file2fix)
        for p in proc_list:
            call(
                [__exec__, fixscript, "-n", "this_elementsenv_base", this_elementsenv_base, p])

    def fix_custom_prefix(self):
        fixscript = os.path.join(self.install_scripts, fixscript_name)
        proc_list = self.get_sysconfig_files()
        proc_list += self.get_config_scripts()
        for p in proc_list:
            call(
                [__exec__, fixscript, "-n", "this_custom_prefix", this_custom_prefix, p])

    def fix_use_custom_prefix(self):
        fixscript = os.path.join(self.install_scripts, fixscript_name)
        proc_list = self.get_sysconfig_files()
        for p in proc_list:
            call(
                [__exec__, fixscript, "-n", "this_use_custom_prefix", this_use_custom_prefix, p])

    def fix_python_version(self):
        fixscript = os.path.join(self.install_scripts, fixscript_name)
        for s in get_script_files():
            if s != fixscript_name:
                full_s = os.path.join(self.install_scripts, s)
                logging.debug("Calling: ", " ".join([__exec__, fixscript,
                                                     "-n", "this_python_version",
                                                     dist_impl_major_version, full_s]))
                call([__exec__, fixscript, "-n", "this_python_version", dist_impl_major_version, full_s])

    def create_extended_init(self):
        init_file = os.path.join(self.install_lib, "ElementsEnv", "__init__.py")

        if not os.path.exists(init_file):
            logging.info("Creating the %s file" % init_file)
            init_content = """# This is the initial setup for the ElementsEnv namespace package
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)  # @ReservedAssignment

"""
            open(init_file, "w").write(init_content)

    def custom_post_install(self):
        self.fix_install_path()
        self.fix_version()
        self.fix_elementsenv_base()
        self.fix_custom_prefix()
        self.fix_use_custom_prefix()
        self.fix_python_version()
        self.create_extended_init()

    def print_install_locations(self):
        print("This is the prefix %s" % self.prefix)
        print("This is the install base %s" % self.install_base)
        print("This is the install platbase %s" % self.install_platbase)
        print("This is the install root %s" % self.root)
        print("This is the install purelib %s" % self.install_purelib)
        print("This is the install platlib %s" % self.install_platlib)
        print("This is the install lib %s" % self.install_lib)
        print("This is the install headers %s" % self.install_headers)
        print("This is the install scripts %s" % self.install_scripts)
        print("This is the install data %s" % self.install_data)

    def run(self):
        _install.run(self)
        # postinstall
        if not skip_custom_postinstall:
#            self.print_install_locations()
            self.custom_post_install()


class PyTest(Command):
    user_options = []
    runtests_filename = "runtests.py"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def _get_python_path():
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(parent_dir, "python")

    @staticmethod
    def _get_scripts_path():
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(parent_dir, "scripts")

    @staticmethod
    def _get_scripts_build_path():
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(parent_dir, "build", "scripts-%s" % sys.version[0:3])

    @staticmethod
    def _get_tests_files():
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        return glob(os.path.join(parent_dir, "tests", "*Test.py"))

    @staticmethod
    def _get_executable_tests_files():
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        tst_list = glob(os.path.join(parent_dir, "tests", "*"))
        return [f for f in tst_list if not os.path.splitext(f)[1] and not os.path.isdir(f)]

    def _generate_runtests_file(self):
        import subprocess
        errno = subprocess.call([pytest_cmd, "--genscript=%s" % self.runtests_filename])
        logging.warning("%s generated. Please consider to add it to your sources" % self.runtests_filename)
        if errno != 0:
            raise SystemExit(errno)

    def run(self):
        import subprocess
        import sys
        sys.path.insert(0, self._get_python_path())
        os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
        from ElementsEnv.Path import envPathPrepend
        envPathPrepend("PATH", self._get_scripts_path())
        envPathPrepend("PATH", self._get_scripts_build_path())
        errno = subprocess.call([pytest_cmd] + self._get_tests_files())
        raise SystemExit(errno)


class MyInstallData(_install_data):
    pass


class MyInstallScripts(_install_scripts):

    def run(self):
        if not self.skip_build:
            self.run_command('build_scripts')
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)
        if os.name == 'posix':
            # Set the executable bits (owner, group, and world) on
            for file in self.get_outputs():
                if  os.path.splitext(file)[1] in [".sh", ".csh"] or os.path.basename(file) == fixscript_name:
                    mode = os.stat(file)[ST_MODE] & ~S_IEXEC
                    log.info("changing mode of %s to %o", file, mode)
                    os.chmod(file, mode)
                else:
                    if self.dry_run:
                        log.info("changing mode of %s", file)
                    else:
                        mode = ((os.stat(file)[ST_MODE]) | 0o555) & 0o7777
                        log.info("changing mode of %s to %o", file, mode)
                        os.chmod(file, mode)


class Purge(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():

        import shutil

        parent_dir = os.path.dirname(os.path.abspath(__file__))

        for d in ["build", "dist"]:
            full_d = os.path.join(parent_dir, d)
            if os.path.exists(full_d):
                logging.info("Removing the %s directory" % full_d)
                shutil.rmtree(full_d)


class Uninstall(Command):

    description = 'Uninstallation of recorded files'
    user_options = [
            ('root=', None, 'path to the root install location'),
        ]

    def initialize_options(self):
        self.root = None

    def finalize_options(self):
        if self.root:
            assert os.path.exists(self.root), "The %s root installation directory doesn't exist" % self.root

    def run(self):

        import shutil
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        record = os.path.join(parent_dir, "dist", "installed_files.txt")
        with open(record) as rf:
            for l in rf:
                f = l.strip()
                if self.root:
                    if f.startswith("/"):
                        f = f[1:]
                    f = os.path.join(self.root, f)
                if os.path.exists(f):
                    if os.path.isdir(f):
                        logging.info("Removing the %s directory" % f)
                        shutil.rmtree(f)
                    else:
                        logging.info("Removing the %s file" % f)
                        os.remove(f)


setup(name=__project__,
      version=__version__,
      description="Elements Environment Scripts",
      author="Hubert Degaudenzi",
      author_email="Hubert.Degaudenzi@unige.ch",
      url="https://github.com/astrorama/ElementsEnv",
      package_dir={"ElementsEnv": os.path.join("python", "ElementsEnv"), },
      packages=["ElementsEnv", "ElementsEnv.Run"],
      scripts=[os.path.join("scripts", s) for s in get_script_files()],
      data_files=etc_files + these_files,
      cmdclass={"install": MyInstall,
                "install_data": MyInstallData,
                "build": MyBuild,
                "sdist": MySdist,
                "bdist_rpm": MyBdistRpm,
                "test": PyTest,
                "purge": Purge,
                "uninstall": Uninstall,
                "build_scripts": MyBuildScripts,
                "install_scripts": MyInstallScripts,
                },
      )
