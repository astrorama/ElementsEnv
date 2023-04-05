# Changelog
All notable changes to this project will be documented in this file. This project
is a companion software for the Elements project. It manges the environment needed to run
the software in a multi-release software tree.

Project Coordinators: Hubert Degaudenzi @hdegaude

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [3.20.0] - 2023-02-14

### Added
- Add CI/CD for CODEEN (Frédéric Leroux)
- Add the ry symbol for Rocky Linux
- Add the full binary tag for Rocky 9 to the list of supported platforms

### Changed
- Move to the [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) format
- Move to the Elements 6.2.0 CMake and Make libraries
- Replacement of the get_python_lib function from distutils
- Convert the Changelog into a "keep a changelog" markdown file
- Move the log warning about the supported configurations to DEBUG
- set the default token in the binary tag to linux instead of lx
  This happens when the distribution is not recognized.
- Update conda recipe for EDEN 3.1 (Frédéric Leroux)

### Removed
- Remove preactivate script : LD_LIBRARY_PATH env var is handled by EDEN direcltly (Frédéric Leroux)
- Remove CMAKEFLAGS from activate.sh. CMAKEFLAGS will be overriden by CT_ElementsProjectDefinition 
  activate script according to local/codeen build (Frédéric Leroux)
- Remove the `tests/__pycache__` directory from the packaging

### Fixed
- Fix the "purelib" prefix by using the sysconfig.get_path('data') call


## [3.18.0] - 2021-04-12

### Changed
- update to the latest make and cmake library of Elements (5.14)


## [3.16.0] - 2020-07-20

### Fixed
- specific release version for Euclid


## [3.16] - 2020-07-20

### Changed
- update to the latest make and cmake library of Elements (5.12)


## [3.14] - 2020-04-30

### Added
- Integration into the jupyter notebooks:
    - add the magic command for ELogin: %elogin
    - Add the draft implementation of the erun magic command
- Add the possibility to run a standalone command with %erun
    - if a command is passed the environment stays untouched
    - otherwise the new environment is imported like before

### Fixed
- fixup of the explicit python in the shebang mangling.


## [3.12.1] - 2020-04-08

### Changed
- update to the latest make and cmake library of Elements (5.10.1)


## [3.12] - 2020-04-07

### Changed
- update to the latest make and cmake library of Elements (5.10)
- Replace distutils by setuptools (Frédéric Leroux)

### Fixed
- various fixes for the python3 (explicit version) and python (implicit)
  version 3 series
- Fix the localisation of the lsb_release utility
- Use relative import to avoid messing around with the PYTHONPATH

### Added
- Modify EuclidWrapper to accept extra config files (Alejandro Alvarez Ayllon).


## [3.10] - 2019-04-12

### Changed
- update to the latest make and cmake library of Elements (5.6)


## [3.8.2] - 2018-10-11

### Fixed
- data/RPM/EuclidEnv.spec.in: fix the spec generation if the python explicit
  version is empty. The RPM post install script were failing in that case
- python/EuclidWrapper/logging.py: fix the absolute import of the system
  logging feature. The EuclidWrapper script was working fine with python3 but
  not with the default system python (python 2)


## [3.8.1] - 2018-08-23

### Fixed
- bypass of the tests in the jenkins CI. Please have look at
  https://euclid.roe.ac.uk/issues/8257


## [3.8] - 2018-08-20

### Added
- add the CTEST_OUTPUT_ON_FAILURE=1 as default environement variable
- add the EuclidWrapper new feature (Nikos)
- implement the python explicit version handling in the scripts.
- add the .jenkinsFile.
- add the full support (distribution and run) for the usage of the

### Removed
- remove the generation of the runtests.py script. The "--genscript"
  option of py.test has been obsoleted
  python3 executable from an unusual location.


## [3.6] - 2018-06-15

### Changed
- update to the latest cmake library of Elements (5.4)


## [3.4] - 2018-03-29

### Fixed
- global fixing of the python 3 explicit version used in the scripts. That
  version is correctly interpolated for every use. Please note that the
  explicit version is detected from the base name of the interpreter which
  is used

### Changed
- the RPM distribution kit (tar.gz and SPEC file) is now using the python
  interpreter fullpath to assert the install root. No on-the-fly rpm relocation
  should be needed then.


## [3.3] - 2017-08-09

### Added
- data/sys/config/euclid: add an extra post script to be sourced called
  EdenEnv.sh. It is looked in the path and should have no side effect if
  it doesn't exist.


## [3.2] - 2017-08-08

### Changed
- update to the latest cmake library of Elements (5.2)


## [3.1.3] - 2017-08-03

### Fixed
- hotfix: remove wrong import in the PlatformTest.py file.


## [3.1.2] - 2017-08-02

### Fixed
- hotfix from Elements 5.1.1 cmake library. There was a typo in the automatic
  dependency generation for the spec files.


## [3.1.1] - 2017-08-28

### Added
- Add the possibility to setup a custom prefix location
- Compile the file (Login.py) which is modified in the RPM postinstall phase
- Make the use prefix flag set automatically if EUCLID_BASE is special. If
  the --relocate option is passed for the /opt/euclid location at the
  rpm install command, the use custom prefix flag is set to "yes" in the
  /etc/sysconfig/euclid. Please note that the --relocate option is just changing
  the EUCLID_BASE location. It doesn't relocate anything.

### Fixed
- Fix a bug which didn't pickup the right project from the user area it has
  been reported at https://euclid.roe.ac.uk/issues/5098 it happens when
    - the version is explicitly asked for: E-Run Elements 5.0.1 ...
    - and the layout of the project has an explicit version directory:
      ~/Work/Projects/Elements/5.0.1 (instead of simply
      ~/Work/Projects/Elements)
   In that case, the /opt/euclid/Elements/5.0.1 was called anyway.

### Changed
- Update to the latest CMake library of Elements (5.1).


## [3.1] - 2017-04-04

### Added
- Add the purge command
- Add the automatic record of the installed files
- Add the uninstall command. It also works with the --root offset

### Fixed
- Fix the guard that avoid that the SAME config file is read twice. Before any
  file pointed by EUCLID_CONFIG_FILE was no reread. That was causing a
  problem of local and CVMFS installations together.


## [3.0] - 2017-03-06

### Changed
- update to the latest cmake library of Elements (5.0)


## [2.1.2] - 2017-02-27

### Fixed
- hotfix of the Euclid.Run.Script module. Remove obsolete buggy part for
  the extra search path implemented in a searchPath.py python file.


## [2.1.1] - 2017-02-24

### Fixed
- hotfix of the Euclid.ConfigFile module.


## [2.1] - 2016-12-16

### Changed
- update to the latest cmake library of Elements (4.1)

### Fixed
- fix up many issues related to the python 3 compatibility.


## [2.0] - 2016-03-22

### Changed
- update to the latest cmake library of Elements (4.0)

### Fixed
- fix bug in ERun autocompletion (Tristan Grégoire)


## [1.15] - 2016-01-25

### Changed
- update to the latest cmake library of Elements (3.10)

### Added
- add ERun_autocompletion.sh script (Tristan Grégoire). Please note
  that this script has to be called by hand from the .bashrc for the moment.


## [1.14.1] - 2015-12-04

### Fixed
- Emergency fix for the usage of EUCLID_BASE env variable in ELogin

### Added
- add a generic lx type in the BINARY_TAG. This corresponds
  to an unkown linux box.


## [1.14] - 2015-11-27

### Changed
- update to the cmake library of Elements 3.9

### Fixed
- fix the cleaning of the ELogin banner
- fix the setup of the environment for bash. Now it is not repeated for
  every subshell.

### Added
- add the new "python setup.py test" command. It is based on a generated
  py.test script.


## [1.13.1] - 2015-10-13

### Fixed
- Bugfix. The E-Run command was not checking the existence of the
  directory of a project before trying to list its version subdirectories.


## [1.13] - 2015-10-07

### Changed
- update to the cmake library of Elements 3.8

### Added
- introduction of the draft generation of the python SWIG bindings


## [1.12.2] - 2015-08-18

### Changed
- update to the cmake library of the Elements 3.7.2 version

### Fixed
- fix a bug in the toolchain crawling of projects


## [1.12.1] - 2015-08-05

### Changed
- update to the cmake library of the Elements 3.7.1 version

### Fixed
- fix of the conversion of the CMAKE_PROJECT_PATH environment variable
  into a cmake list


## [1.12] - 2015-08-03

### Changed
- update the cmake library to the Elements 3.7 version

### Fixed
- fix the E-Run command to work with the User_area without version
  directory.


## [1.11] - 2015-06-15

### Changed
- update the cmake library to the Elements 3.6 version.

### Added
- contains the CMake Bootstrap Toolchain.


## [1.10] - 2015-02-26

### Changed
- update the cmake library to the Elements 3.5 version.

### Fixed
- fixes for the MacPort warnings.


## [1.9] - 2015-02-02

### Changed
- update the cmake library to the Elements 3.4 version.

### Fixed
- various fixes for the Darwin platform.

### Added
- new version of the latex class with the new Euclid logo.


## [1.8] - 2014-11-07

### Changed
- updated the cmake library to the Elements 3.3 version.


## [1.7] - 2014-10-13

### Changed
- updated to the Elements 3.2 cmake library.

### Fixed
- fixed the version extraction from the SVN tags.


## [1.6] - 2014-10-06

### Changed
- imported the cmake library from Elements 3.1

### Fixed
- fixed the User_area location default from ~/Work to ~/Work/Projects.


## [1.5] - 2014-08-28

### Changed
- adapted from Elements 3.0

### Removed
- mostly a removal of the win32 part


## [1.4] - 2014-07-14

### Fixed
- Fix the default BINARY_TAG and set it to the RelWithDebugInfo type.
- Cure the logic for the full setup of the ELogin wrapper. It is done if
  the shell is either a login one or non-interactive.

### Added
- Add the "--implicit-latest" option to E-Run.


## [0.0.0] - 2016-01-01

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
