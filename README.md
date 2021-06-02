# README

## Notes

1. In order to create the source tarball suitable for the creation of RPM, 2 commands are possible:

   ```
   git archive --format=tar.gz --prefix=ElementsEnv-0.2/ --output ~/.local/tmp/rpmbuild/SOURCES/ElementsEnv-0.2.tar.gz 0.2
   ```
   or

   ```
   python setup.py sdist
   ```

1. Please note that this script cannot be used for the RPM creation.
   the "python setup.py bdist_rpm" doesn't equip the spec file with the
   proper post install command. For the rpm creation the SPEC file ad
   hoc file provided in data/RPM directory

   it can be used for :
   * the creation of a source tarball "python setup.py sdist" suitable for
     the RPM creation
   * the direct install "python setup.py install ..."

1. The created RPM file is relocatable through 3 folders

   ```
   rpm -Uvh --relocate /etc/=/home/hubert/.local/tmp/testrpm \
            --relocate /usr=/home/hubert/.local/tmp/testrpm \
            --relocate /opt=/home/hubert/.local/tmp/testrpm  
            ../RPMS/noarch/ElementsEnv-0.3-1.fc19.noarch.rpm
   ```

1. The direct installation with the "python setup.py install" support several
   schemes (--home, --prefix, --root, --user) and options. The schemes are the
   default ones supported by the python distutils package and the special options
   are:
   * `--skip-custom-postinstall`: to avoid the postinstall treatment. Useful when
      creating RPMs
   * `--elementsenv-base`: to specify the native ElementsEnv Software installation base. This will
      trigger a post install script to hardcode the location in the scripts.

   Typical call are:
   1. `python setup.py install  --user --elementsenv-base=/my/custom/dir`

      That will use the common user python installation for ElementsEnv and set
      the default ElementsEnv software location to /my/custom/dir

   1. `python setup.py install --prefix=~/Work/Env --elementsenv-base=/my/custom/dir`

      This will do the same as the previous one, except that the very installation
      of the ElementsEnv package will be done at a custom prefix location.
