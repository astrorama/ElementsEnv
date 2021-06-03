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
command is also aliased to `ERun`.

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

and that can be translated into (if we use the `$HOME/Work/Projects`
directory as prefix for the installation path):

    tar zxvf ElementsEnv-1.4.tar.gz
    cd ElementsEnv-1.4
    mkdir -p $HOME/Work/Projects
    python setup.py install --prefix=$HOME/Work/Projects

As for the RPM installation the last step running the `setup.py` script
is necessary. It runs a post install script that sets the very install
location in the scripts. The layout of the installed files is described
\[\[UserManual\#For-Local-Installation|here\]\].

### The Structure of the Installation

The structure of the installed software for both local installation and
RPM system installation is described in the following table:

| File Type            | Standard Installation                     | Local Installation                                   |
| -------------------- | ----------------------------------------- | ---------------------------------------------------- |
| profile scripts      | `/etc/profile.d/elementsenv.{,c}sh`            | `<install_prefix>/etc/profile.d/elementsenv.{,c}sh`       |
| config file          | `/etc/sysconfig/elementsenv`                   | `<install_prefix>/etc/sysconfig/elementsenv`              |
| executable directory | `/usr/bin`                                | `<install_prefix>/bin`                               |
| python modules       | `/usr/lib/python2.7/site-packages/ElementsEnv` | `<install_prefix>lib/python2.7/site-packages/ElementsEnv` |
| CMake library        | `/usr/share/ElementsEnv/cmake`              | `<install_prefix>/share/ElementsEnv/cmake`             |
| LaTeX files          | `/usr/share/ElementsEnv/texmf`              | `<install_prefix>/share/ElementsEnv/texmf`             |

From the previous example we have `<install_prefix>=$HOME/Work/Projects`

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

The quick way to setup the base ElementsEnv development environment is done
by sourcing the ELogin script for your shell type. For the csh-like
shells, the command looks like:

    source `/usr/bin/which ELogin.csh`

  
and for the sh-like shell:

    source `/usr/bin/which ELogin.sh`

For the \[\[UserManual\#Local-Custom-Installation|custom
installation\]\], the full path to the scripts
(`<install_prefix>/bin/ELogin.{,c}sh`) has to be explicitly given. For
the csh-like:

    source $HOME/Work/ElementsEnv/bin/ELogin.csh

  
and for the sh-like:

    source $HOME/Work/ElementsEnv/binELogin.sh

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
different cases, 2 wrappers have been written : `ElementsEnv_group_login.sh`
and `ElementsEnv_group_setup.sh`. They will provide respectively the “full
login” and “shell setup only” feature that are mentioned above. ie :

1.  The **login part** is called from the `.bash_profile` file like: 
        source <install_prefix>/bin/ElementsEnv_group_login.sh 
2.  The **shell only part** is called from the `.bashrc` file like:
        source <install_prefix>/bin/ElementsEnv_group_setup.sh

While wrapping up the direct call the the `ELogin.sh` script, these 2
wrappers provide some extra features that are described below.

#### The Configuration File

The group login and group setup wrapper scripts are reading the base
configuration file. It contains:

    ELEMENTSENV_BASE=/opt
    ELEMENTSENV_USE_BASE=no

  
The `ELEMENTSENV_BASE` environment variable points to the main installation
location of the ElementEnv software projects (like Elements and Alexandria).
Its default value is `/opt`. The `ELEMENTSENV_USE_BASE` is only used
internally.

The location of the configuration file is shown in the table for the
structure of the installation above : it is either
`/etc/sysconfig/elementsenv` for the standard installation or
`<install_prefix>/etc/sysconfig/elementsenv` for the local installation.

### The Profile Setup

For the standard installation, there is an easy way to provide an
automatic setup of the environment. This is through the profile
mechanism.

Each shell at startup reads some mandatory system config files that in
turn read source the files of the `/etc/profile.d` directory. In that
directory there are files for both `sh` and `csh` families of shells.
And this is not different for the `/etc/profile.d/elementsenv.sh` and
`/etc/profile.d/elementsenv.csh` files. They are read whenever a new shell is
created.

And these latter files reads the correct file at the correct moment. For
the login procedure they source the `ElementsEnv_group_login.{,c}sh` files
and for the subshell creation, the `ElementsEnv_group_setup.{,c}sh` files

### The Manual Setup

If you don’t have a full standard installation, you will have to call
the scripts by hand. There will be one sourced from the login
configuration file and one sourced from the shell configuration part.

For tcsh, this is rather easy just put

    source <install_prefix>/bin/ElementsEnv_group_login.csh

in the `$HOME/.login` file and

    source <install_prefix>/bin/ElementsEnv_group_setup.csh

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
    
    source <install_prefix>/bin/ElementsEnv_group_login.sh

and for the `$HOME/.bashrc`:

    # .bashrc
    
    # Source global definitions
    if [ -f /etc/bashrc ]; then
        . /etc/bashrc
    fi
    
    # User specific aliases and functions
    
    ...
    ...
    
    
    source <install_prefix>/bin/ElementsEnv_group_setup.sh

## Customisation

### Inhibiting the Automatic Setup

To prevent the automatic setup to be launched, one can create a single
file that can prevent the wrapper scripts
(`ElementsEnv_group_{login,setup}.{,c}sh`) to do anything:

    touch $HOME/.noElementsEnvLoginScript

This is really useful for debugging system installation of ElementsEnv
with RPM for example.

Please note that the `ELogin.{,c}sh` scripts are **not** influenced by
this file.

### Using Your Own Global Configuration

The script that searches for the global configuration of the ElementsEnv
package looks for these files in the following order:

1.  `$XDG_CONFIG_HOME/ElementsEnv/default` (if `XDG_CONFIG_HOME` exists)
2.  `$HOME/.config/ElementsEnv/default`
3.  for f in `$XDG_CONFIG_DIRS` : `$f/ElementsEnv/default`
4.  `/etc/default/ElementsEnv`
5.  `/etc/sysconfig/elementsenv`
6.  `<prefix>/etc/sysconfig/elementsenv`

The script uses the first file that exists. The search is also
completely skipped if the `ELEMENTSENV_CONFIG_FILE` environment variable is
defined. It has to point to a valid configuration file.

It is important to note that the search and reading of the global
configuration file is only done in `/etc/profile.d/elementsenv.sh`,
`ElementsEnv_group_login.{,c}sh` and `ElementsEnv_group_setup.{,c}sh`. It is not
used when calling the shallow wrapper `ELogin.{,c}sh`. In the later
case, the variables defined for the configuration have to be set
beforehand.

### The Content of the Configuration File

As described above one of the only meaningful variable that is defined
in the configuration file is the `ELEMENTSENV_BASE` location. It has to point
to the top location containing the Elements-based projects. Namely the
structure of the software tree must look like:

    $ELEMENTSENV_BASE/Elements/1.3
    $ELEMENTSENV_BASE/Elements/2.2
    $ELEMENTSENV_BASE/Alexandria/2.0
    ...

  
Please note that the `ELEMENTSENV_BASE` location can be completely
independent from the `<install_prefix>` location.

The other setting that the configuration file can contain is a locale
site tuning script.

### Local Site Tunning

The configuration can also contain the variable `ELEMENTSENV_POST_SCRIPT`.
This variable has to point to the absolute location of a locate
customization script. This script should contains some specific
environment variable to be set for the site tailoring. Therefore it has
to be a script “to be sourced” with an “sh” or “csh” extension.

Actually both `sh` and `csh` are needed and it should appear without
extension in the configuration file:

    ELEMENTSENV_BASE=/opt
    ELEMENTSENV_USE_BASE=no
    ELEMENTSENV_POST_SCRIPT=${ELEMENTSENV_BASE}/scripts/my_site

  
and the `/opt/scripts/my_site.sh` and
`/opt/scripts/my_site.csh` should be written accordingly for the
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

  - —— ElementsEnv Login —— \*
  - Building with gcc48 on fc19 x86\_64 system (x86\_64-fc19-gcc48-o2g)
    \*  
    ****  
    —- User\_area is set to /home/isdc/degauden/Work/Space/Projects 
    —- ELEMENTSENVPROJECTPATH is set to:  
    /opt
    ————————————————————————————————————————  
    \[degauden@piecld00:\~\] which ELogin  
    ELogin=‘. \`/usr/bin/which ELogin.sh\`’  
    \[de

