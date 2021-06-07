ElementsEnv is a python package that can be used as a companion software for the development of Elements-based software projects. It allows to builds and use several version of the same project in a consistent way. 

For this purpose, ElementsEnv provides 2 executable:
* **ELogin** that sets up the build environment. It has to be called before anything else and it might be interesting to have called by the shell login script. Please have a look at the [user manual](doc/Manual.md) for more details.
* **E-Run** (**ERun**) that enables to call the executable of any version of any reachable project

## Quick Install

1. Once the source tarball has been downloaded and expanded, the user installation of the software can be done with the usual `setup.py` script.
   ```
   python setup.py install --user
   ```
   This will perform the installation in various sub-directories of the home directory of the user. This will install the `ELogin` and `E-Run` scripts.

## Setup

1. After this installation, the executables are placed in the `~/.local/bin` directory. Therefore, this directory has to be preprended manually to the PATH environment variable in the profile script of the user's shell (`.bash_profile` for bash and `.login` for tcsh). 

1. To initialize the build environment (and thus being able to access the `E-Run` command and the `ELogin` alias), the `ELogin.sh` (or `ELogin.csh` for the csh shell family) needs to be sourced. 
   * For the bash shell family (bash, zsh), there are 2 possibilities:
     ```
     source ~/.local/bin/ELogin.sh
     ```
     or 
     ```
     . ELogin.sh
     ```
     The `.` command will do the lookup in the PATH environment variable, but the `source` command doesn't.
   * For the csh shell family (csh, tcsh):
     ```
     source ~/.local/bin/ELogin.csh
     ```
     After the sourcing above, the `ELogin` alias will be available. It will facilitate the sourcing of the `ELogin.sh` file and looks like:
     ```
     alias ELogin="source `which ELogin.sh`"
     ```
     ```
     alias ELogin "source `which ELogin.csh`"
     ```
     
     
## Usage

After the setup done by the sourcing of `ELogin.sh`, the E-Run command will be available. It allows to call any executable for the Elements-based projects located in the `CMAKE_PROJECT_PATH`. This environment variable defaults to `~/Work/Projects:/opt`. The trailing `/opt` location can be tuned at the insallation time of the ElmeentsEnv package. Please have a look at the [user manual](doc/Manual.md) for more details.

The call to any executable of a specific version of a given project is then:
```
E-Run MyProject 1.2 MyExec arg1 arg2 ...
```

The locations of the source trees of the various projects would look like, in general:
  ```
  ~/Work/Projects/MyProject/1.2
  ~/Work/Projects/MyProject/1.3
  /opt/MyProject/1.0
  /opt/MyProject/1.2
  /opt/MySecondProject/0.1
  ...
  ``` 

### Remarks

* The lookup is always done in the order of the CMAKE_PROJECT_PATH locations. The fist match wins.
* The version sub-directory is not mandatory. The project root can be simply located at `~/Work/Projects/MyProject`. In that case, obviously, only one version of the project MyProject can be used. It is only possible in the `~/Work/Projects` location (and not in the `/opt` location).
* The version _keyword_ in the E-Run command line can be ommitted:
  ```
  E-Run MyProject MyExec arg1 arg2 ...
  ```
  In that situation, either the highest version of the project in the current location is selected or the versionless project.


---

## Packaging

1. In order to create the source tarball suitable for the creation of RPM, 2 commands are possible:

   ```
   git archive --format=tar.gz --prefix=ElementsEnv-0.2/ --output $(rpm --eval "%_sourcedir")/ElementsEnv-0.2.tar.gz 0.2
   ```
   or

   ```
   python setup.py sdist
   ```
   
   This last command also generates the needed RPM spec file for the RPM package creation in the dist sub-directory.

1. Please note that this `setup.py` script cannot be used for the RPM creation directly.
   the "python setup.py bdist_rpm" doesn't equip the spec file with the
   proper post install command. The RPM spec file is generated from a template located in the data/RPM sub-directory. 
   
   The RPM packages can then be created with
   
   ```
   # cp dist/ElementsEnv-0.2.tar.gz $(rpm --eval "%_sourcedir")/
   # cp dist/ElementsEnv.spec $(rpm --eval "%_specdir")/
   # cd ElementsEnv-0.2.tar.gz 
   # rpmbuild -ba ElementsEnv.spec
   ```

## Installation


1. The created RPM file is relocatable through 3 folders

   ```
   rpm -Uvh --relocate /etc/=/home/hubert/.local/tmp/testrpm \
            --relocate /usr=/home/hubert/.local/tmp/testrpm \
            --relocate /opt=/home/hubert/.local/tmp/testrpm  
            ../RPMS/noarch/ElementsEnv-0.3-1.fc19.noarch.rpm
   ```

1. The direct installation with the "python setup.py install" support several
   schemes (`--home`, `--prefix`, `--root`, `--user`) and options. The schemes are the
   default ones supported by the python distutils package and the special options
   are:
   * `--skip-custom-postinstall`: to avoid the postinstall treatment. Useful when
      creating RPMs
   * `--elementsenv-base`: to specify the native ElementsEnv Software installation base. This will trigger a post install script to hardcode the location in the scripts. The default location is `/opt`.

   Typical call are:
   1. `python setup.py install  --user --elementsenv-base=/my/custom/dir`

      That will use the common user python installation for ElementsEnv and set
      the default ElementsEnv software location to /my/custom/dir
      
      By default, `python setup.py install  --user` will use `/opt` for the default installation of the Elements-based software projects that this package will manage.
      
      ElementsEnv itself, in the case of the `--user` option will install its executables in the `~/.local/bin` directory. In order to be able to access them, that directory needs to be added to the PATH environment variable in the user's login script.
      

   1. `python setup.py install --prefix=~/Work/Env --elementsenv-base=/my/custom/dir`

      This will do the same as the previous one, except that the very installation
      of the ElementsEnv package will be done at a custom prefix location.
       
 


