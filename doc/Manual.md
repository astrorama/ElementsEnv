# [[ElementsEnv]] User Manual

# User Manual

## Introduction

The goal of the ElementsEnv software project is to provide a convenient
way to develop and run the software projects based on the
Elements framework. It provides the needed environment for their
development and execution.

The reason for the need of such special piece of software like ElementsEnv
origins in the very flexibility features of the Elements project. This
framework allows to deploy the software projects (like Elements
or Alexandria) in several custom places and it also allows to
deploy several versions of the same software project. It means that the
various components of the project (libraries, header files, executables,
python modules etc) have to be located dynamically at build time and at
run time. This is exactly ElementsEnv’s job.

### `ELogin`

The fundamental script of the ElementsEnv project is `ELogin`. This script
has to be sourced and it provides the needed environment. A few
environment variables:

  - `BINARY_TAG` : the guessed platform configuration
  - `CMAKE_PREFIX_PATH` : the bootstrap location of the CMake build
    library
  - `CMAKE_PROJECT_PATH` : the location of the projects

After the sourcing of this script, the system is ready for the building
of Elements-based software projects.

### `E-Run`

For the runtime, in order to run any executable of any project with the
correct environment: the `E-Run` script that generates automatically the
runtime environment (`PATH`, `LD_LIBRAY_PATH`, `PYTHONPATH`,
`ELEMENTS_AUX_PATH` and `ELELEMTS_CONF_PATH`) and runs the command. This
command is also aliased to `EuclidRun` and `ERun`.

This command has to be run explicitly for any executable that you would
like to run in the environment of any project. For example

    E-Run Alexandria 2.0 Catalog_test

This will run the `Catalog_test` executable from the version 2.0 of the
Alexandria project if it is anywhere to be found in the
`CMAKE_PROJECT_PATH` collection of paths. The `E-Run` depends on the
base environment set up by `ELogin` to locate the projects and to use
the right binary tag.

## Download and Install

The installation of the ElementsEnv package can be done in 2 ways:

  - with the RPM package format — this is essentially for the Linux
    RedHat-like platform,
  - or with the custom local installation from the source tarball. 

The first method being quite adequate for development or production
servers and the second one is more suited for custom installation on a
laptop and/or a non-RPM based installation system.

### Installation of the Official RPM package

The RPM files to be installed (like
[ElementsEnv-1.4-1.fc19.noarch.rpm](https://redmine.isdc.unige.ch/attachments/download/277/ElementsEnv-1.4-1.fc19.noarch.rpm\))
are located in the [Files
section](https://redmine.isdc.unige.ch/projects/ElementsEnv/files) of this
project. A more up-to-date version of this list can also be accessed on
the [genuine repository
location](http://degauden.isdc.unige.ch/euclid/repo/fedora/19/x86_64/).

These ElementsEnv RPM files can be downloaded installed in the usual way
by using the `yum` command for example:

    wget http://degauden.isdc.unige.ch/euclid/repo/fedora/19/x86_64/ElementsEnv-1.4-1.fc19.noarch.rpm
    sudo yum localinstall ElementsEnv-1.4-1.fc19.noarch.rpm

  
This is an example for the Fedora 19 platform.

A more convenient and *recommended* way is to install the Repo RPM that
will configure the repository on the target machine:

    wget http://degauden.isdc.unige.ch/euclid/repo/fedora/19/x86_64/EuclidRepo-0.1-1.noarch.rpm
    sudo yum localinstall EuclidRepo-0.1-1.noarch.rpm
    sudo yum install ElementsEnv

  
This will provide a more easy way to update the software:

    sudo yum update ElementsEnv

  
or simply

    sudo yum update

  
that will trigger the update of the whole system.

Please note that the installation of these packages is not just the
deployment of the files: some post-processing has to be done to fix the
install location. The layout of the installed files is described
\[\[UserManual\#For-Standard-System-Installation|here\]\].

### Local Custom Installation

For more that one reason, the installation of the software by RPM
packages is not possible. Essentially on system that do not support RPM
at all. This can also be quite useful as well on servers where the user
of the package is not root and would like to use the ElementsEnv software
locally.

Typically, this would be the case for the installation on a MacOSX
laptop.

In this situation, the procedure looks like:

1.  download the compressed tarball
2.  uncompress and untar it
3.  choose a target directory
4.  run the install script

and that can be translated into (if we use the `$HOME/Work/Euclid`
directory as prefix for the installation path):

    wget http://degauden.isdc.unige.ch/euclid/repo/sources/ElementsEnv-1.4.tar.gz
    tar zxvf ElementsEnv-1.4.tar.gz
    cd ElementsEnv-1.4
    mkdir -p $HOME/Work/Euclid
    python setup.py install --prefix=$HOME/Work/Euclid

As for the RPM installation the last step running the `setup.py` script
is necessary. It runs a post install script that sets the very install
location in the scripts. The layout of the installed files is described
\[\[UserManual\#For-Local-Installation|here\]\].

### The Structure of the Installation

The structure of the installed software for both local installation and
RPM system installation is described in the following table:

| File Type            | Standard Installation                     | Local Installation                                   |
| -------------------- | ----------------------------------------- | ---------------------------------------------------- |
| profile scripts      | `/etc/profile.d/euclid.{,c}sh`            | `<install_prefix>/etc/profile.d/euclid.{,c}sh`       |
| config file          | `/etc/sysconfig/euclid`                   | `<install_prefix>/etc/sysconfig/euclid`              |
| executable directory | `/usr/bin`                                | `<install_prefix>/bin`                               |
| python modules       | `/usr/lib/python2.7/site-packages/Euclid` | `<install_prefix>lib/python2.7/site-packages/Euclid` |
| CMake library        | `/usr/share/ElementsEnv/cmake`              | `<install_prefix>/share/ElementsEnv/cmake`             |
| LaTeX files          | `/usr/share/ElementsEnv/texmf`              | `<install_prefix>/share/ElementsEnv/texmf`             |

From the previous example we have `<install_prefix>=$HOME/Work/Euclid`

Remarks:

  - Except for the profile scripts, all the other scripts are located in
    the `bin` subdirectory.
  - The scripts are sourced and that is the reason why they come in 2
    flavors, `sh` and `csh` depending on the shell that you use. Many
    examples in this manual are using the `sh` version only for
    conciseness but the `csh` can be used as well.
  - For the standard installation, the scripts are located by default in
    the `PATH` environment variable at the `/usr/bin` location. They can
    thus be easily located by the `which` command and thus, we can call
    them with:
        source `/usr/bin/which <script>.sh`
    Please note that the `which` command is the one from the system, not
    an alias of the shell.
  - For the local installation, the scripts have to be addressed with
    their full path:
        source <install_prefix>/bin/<script>.sh
  - For the local installation, the initial setup done with the
    `ELogin.sh` script updates the environment part that was not needed
    for the standard installation
        PATH=<install_prefix>/bin:$PATH
        PYTHONPATH=<install_prefix>/lib/python2.7/site-packages:$PYTHONPATH
  - For both local and standard installation, the following environment
    variable are updated:
        TEXINPUTS=<install_prefix>/share/ElementsEnv/texmf:$TEXINPUTS                 # For local installation 
        TEXINPUTS=/usr/share/ElementsEnv/texmf:$TEXINPUTS                             # For standard installation
        CMAKE_PREFIX_PATH=<install_prefix>/share/ElementsEnv/cmake:$CMAKE_PREFIX_PATH # For local installation
        CMAKE_PREFIX_PATH=/usr/share/ElementsEnv/cmake:$CMAKE_PREFIX_PATH             # For standard installation

### Quick Setup

The quick way to setup the base Euclid development environment is done
by sourcing the ELogin script for your shell type. For the csh-like
shells, the command looks like:

    source `/usr/bin/which ELogin.csh`

  
and for the sh-like shell:

    source `/usr/bin/which ELogin.sh`

For the \[\[UserManual\#Local-Custom-Installation|custom
installation\]\], the full path to the scripts
(`<install_prefix>/bin/ELogin.{,c}sh`) has to be explicitly given. For
the csh-like:

    source $HOME/Work/Euclid/bin/ELogin.csh

  
and for the sh-like:

    source $HOME/Work/Euclid/binELogin.sh

It is worth noting that a new aliases is available after this sourcing.
For csh-like shells:

    alias ELogin
    > ELogin source `/usr/bin/which ELogin.csh`

  
and for sh-like shells:

    alias ELogin
    > ELogin='. `/usr/bin/which  ELogin.sh`'

More sophisticate calls to `ELogin` are detailed in the
\[\[UserManual\#ELogin-2|tools section\]\].

## Full Persistent Setup with Wrapper Scripts

Instead of sourcing directly and always the main `ELogin.{,c}sh` script,
a set of convenient wrappers have been provided to make it more
efficient.

In details the setup of the full environment, which is in most cases
unneeded, can be tuned to be as light as possible. This can be done by
**splitting the files used for the initialization of a full login
session and the initialisation of a subshell only**. In the later case,
the environment variables are inherited from the main parent shell and
only the shallow setup of the core shell is needed. That second setup is
usually only aliases for for the ELogin procedure. To summarize:

1.  The **login part** is called like 
        source <install_prefix>/bin/ELogin.sh 
    This will provide the full environment. With both environment
    variables and aliases
2.  The **shell only part** is called like:
        source <install_prefix>/bin/ELogin.sh --shell-only --silent
    This will provide the shell onyl part, namely only the aliases.

These 2 parts have to be called by the shell initialization files. The
first part from the `.bash_profile` file and the second one from the
`.bashrc` file.

### The Group Login and Group Setup Wrappers

In order to simplify the usage of the `ELogin.sh` script in the 2
different cases, 2 wrappers have been written : `Euclid_group_login.sh`
and `Euclid_group_setup.sh`. They will provide respectively the “full
login” and “shell setup only” feature that are mentioned above. ie :

1.  The **login part** is called from the `.bash_profile` file like: 
        source <install_prefix>/bin/Euclid_group_login.sh 
2.  The **shell only part** is called from the `.bashrc` file like:
        source <install_prefix>/bin/Euclid_group_setup.sh

While wrapping up the direct call the the `ELogin.sh` script, these 2
wrappers provide some extra features that are described below.

#### The Configuration File

The group login and group setup wrapper scripts are reading the base
configuration file. It contains:

    EUCLID_BASE=/opt/euclid
    EUCLID_USE_BASE=no

  
The `EUCLID_BASE` environment variable points to the main installation
location of the Euclid software projects (like Elements and Alexandria).
Its default value is `/opt/euclid`. The `EUCLID_USE_BASE` is only used
internally.

The location of the configuration file is shown in the table for the
structure of the installation above : it is either
`/etc/sysconfig/euclid` for the standard installation or
`<install_prefix>/etc/sysconfig/euclid` for the local installation.

### The Profile Setup

For the standard installation, there is an easy way to provide an
automatic setup of the environment. This is through the profile
mechanism.

Each shell at startup reads some mandatory system config files that in
turn read source the files of the `/etc/profile.d` directory. In that
directory there are files for both `sh` and `csh` families of shells.
And this is not different for the `/etc/profile.d/euclid.sh` and
`/etc/profile.d/euclid.csh` files. They are read whenever a new shell is
created.

And these latter files reads the correct file at the correct moment. For
the login procedure they source the `Euclid_group_login.{,c}sh` files
and for the subshell creation, the `Euclid_group_setup.{,c}sh` files

### The Manual Setup

If you don’t have a full standard installation, you will have to call
the scripts by hand. There will be one sourced from the login
configuration file and one sourced from the shell configuration part.

For tcsh, this is rather easy just put

    source <install_prefix>/bin/Euclid_group_login.csh

in the `$HOME/.login` file and

    source <install_prefix>/bin/Euclid_group_setup.csh

in the `$HOME/.tcshrc` file and

Because it initialized a bit differently, the things are a bit more
complex for bash: The `$HOME/.bash_profile$` has to follow its main
skeleton has to look like:

    # .bash_profile
    
    # Get the aliases and functions
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi
    
    # User specific environment and startup programs
    
    ...
    ...
    
    source <install_prefix>/bin/Euclid_group_login.sh

and for the `$HOME/.bashrc`:

    # .bashrc
    
    # Source global definitions
    if [ -f /etc/bashrc ]; then
        . /etc/bashrc
    fi
    
    # User specific aliases and functions
    
    ...
    ...
    
    
    source <install_prefix>/bin/Euclid_group_setup.sh

## Customisation

### Inhibiting the Automatic Setup

To prevent the automatic setup to be launched, one can create a single
file that can prevent the wrapper scripts
(`Euclid_group_{login,setup}.{,c}sh`) to do anything:

    touch $HOME/.noEuclidLoginScript

This is really useful for debugging system installation of ElementsEnv
with RPM for example.

Please note that the `ELogin.{,c}sh` scripts are **not** influenced by
this file.

### Using Your Own Global Configuration

The script that searches for the global configuration of the ElementsEnv
package looks for these files in the following order:

1.  `$XDG_CONFIG_HOME/Euclid/default` (if `XDG_CONFIG_HOME` exists)
2.  `$HOME/.config/Euclid/default`
3.  for f in `$XDG_CONFIG_DIRS` : `$f/Euclid/default`
4.  `/etc/default/Euclid`
5.  `/etc/sysconfig/euclid`
6.  `<prefix>/etc/sysconfig/euclid`

The script uses the first file that exists. The search is also
completely skipped if the `EUCLID_CONFIG_FILE` environment variable is
defined. It has to point to a valid configuration file.

It is important to note that the search and reading of the global
configuration file is only done in `/etc/profile.d/euclid.sh`,
`Euclid_group_login.{,c}sh` and `Euclid_group_setup.{,c}sh`. It is not
used when calling the shallow wrapper `ELogin.{,c}sh`. In the later
case, the variables defined for the configuration have to be set
beforehand.

### The Content of the Configuration File

As described above one of the only meaningful variable that is defined
in the configuration file is the `EUCLID_BASE` location. It has to point
to the top location containing the Elements-based projects. Namely the
structure of the software tree must look like:

    $EUCLID_BASE/Elements/1.3
    $EUCLID_BASE/Elements/2.2
    $EUCLID_BASE/Alexandria/2.0
    ...

  
Please note that the `EUCLID_BASE` location can be completely
independent from the `<install_prefix>` location.

The other setting that the configuration file can contain is a locale
site tuning script.

### Local Site Tunning

The configuration can also contain the variable `EUCLID_POST_SCRIPT`.
This variable has to point to the absolute location of a locate
customization script. This script should contains some specific
environment variable to be set for the site tailoring. Therefore it has
to be a script “to be sourced” with an “sh” or “csh” extension.

Actually both `sh` and `csh` are needed and it should appear without
extension in the configuration file:

    EUCLID_BASE=/opt/euclid
    EUCLID_USE_BASE=no
    EUCLID_POST_SCRIPT=${EUCLID_BASE}/scripts/my_site

  
and the `/opt/euclid/scripts/my_site.sh` and
`/opt/euclid/scripts/my_site.csh` should be written accordingly for the
tuning.

## The Tools

There are 2 main tools that are present in the ElementsEnv software
package. Both are scripts that can modify the environment of the user.
The first one, `ELogin` is meant to be used at login time and provide
the base environment for the development of software based on Elements.
It also provide access to the second tool, `E-Run`.

The `E-Run` script provide the runtime environment for a given
Elements-based software project (like Alexandria for example) instance.
It is not meant to be setup at login time but provide a convenient way
to enable the environment variables needed by the project instance.

Both of these tools are equipped with a `--help` that will provide some
rather compact info.

### ELogin

The ELogin command (the alias) is only available when a full login *has
already been done*. ie:

<pre>

-----

  - —— Euclid Login —— \*
  - Building with gcc48 on fc19 x86\_64 system (x86\_64-fc19-gcc48-o2g)
    \*  
    ****  
    —- User\_area is set to /home/isdc/degauden/Work/Space/Euclid  
    —- EUCLIDPROJECTPATH is set to:  
    /opt/euclid  
    ————————————————————————————————————————  
    \[degauden@piecld00:\~\] which ELogin  
    ELogin=‘. \`/usr/bin/which ELogin.sh\`’  
    \[de

