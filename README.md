ElementsEnv is a python package that can be used as a companion software for the development of Elements-based software projects. It allows to builds and use several version of the same project in a consistent way. 

For this purpose, ElementsEnv provides 2 executable:
* **ELogin** that sets up the build environment. It has to be called before anything else and it might be interesting to have called by the shell login script. Please have a look at the [user manual](doc/Manual.md) for more details.
* **E-Run** (**ERun**) that enables to call the executable of any version of any reachable project

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
       
 


