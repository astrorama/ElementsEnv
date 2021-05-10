# default file to be tested in order
# 1) $XDG_CONFIG_HOME/ElementsEnv/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/ElementsEnv/default
# 3) for f in $XDG_CONFIG_DIRS : $f/ElementsEnv/default
# 4) %(this_etc_install_prefix)s/default/ElementsEnv
# 5) %(this_etc_install_prefix)s/sysconfig/elementsenv
# 6) /etc/default/ElementsEnv
# 7) /etc/sysconfig/elementsenv

my_own_prefix0="%(this_etc_install_prefix)s"
my_own_exe_prefix0="%(this_install_prefix)s"

cfgfiles=""

if [[ ! -e ${HOME}/.noElementsEnvUserConfig ]]; then
  if [[  -n "$XDG_CONFIG_HOME" ]]; then
    cfgfiles="$cfgfiles $XDG_CONFIG_HOME/ElementsEnv/default"
  fi
  if [[ -n "$HOME" ]]; then
    cfgfiles="$cfgfiles $HOME/.config/ElementsEnv/default"
  fi
fi

if [[ -n "$XDG_CONFIG_DIRS" ]]; then
  for d in $(echo $XDG_CONFIG_DIRS | tr -s ':' ' ')
  do
    cfgfiles="$cfgfiles $d/ElementsEnv/default"
  done
  unset d
fi
cfgfiles="$cfgfiles $my_own_prefix0/default/ElementsEnv"
cfgfiles="$cfgfiles $my_own_prefix0/sysconfig/ElementsEnv"
cfgfiles="$cfgfiles /etc/default/ElementsEnv"
cfgfiles="$cfgfiles /etc/sysconfig/ElementsEnv"

elementsenv_config_file_current=""
for c in $(echo $cfgfiles)
do
  if [[ -r $c ]]; then
    elementsenv_config_file_current=$c
    break;
  fi
done

unset c
unset cfgfiles

if [[ ! "${ELEMENTSENV_CONFIG_FILE}" = "${elementsenv_config_file_current}" ]]; then

# default values if no config file is found
export SOFTWARE_BASE_VAR=ELEMENTSENV_BASE
export ELEMENTSENV_BASE=%(this_elementsenv_base)s
export ELEMENTSENV_USE_BASE=no
export ELEMENTSENV_USE_PREFIX=no
export ELEMENTSENV_CUSTOM_PREFIX=%(this_elementsenv_base)s/../../usr
export ELEMENTSENV_USE_CUSTOM_PREFIX=no

if [[ -n "${elementsenv_config_file_current}" ]]; then
  eval `cat ${elementsenv_config_file_current} | sed -n -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/\1="\2"; export \1;/gp'`
fi

export ELEMENTSENV_CUSTOM_PREFIX=$(readlink -m ${ELEMENTSENV_CUSTOM_PREFIX})

arch_type=`uname -m`

# prepend path entries from the base to the environment
if [[ "${ELEMENTSENV_USE_BASE}" == "yes" ]]; then
  if [[ -d ${ELEMENTSENV_BASE} ]]; then
    
    if [[ -d ${ELEMENTSENV_BASE}/bin ]]; then
      export PATH=${ELEMENTSENV_BASE}/bin:${PATH}
    fi
    if [[ -d ${ELEMENTSENV_BASE}/scripts ]]; then
      export PATH=${ELEMENTSENV_BASE}/scripts:${PATH}
    fi
    
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${ELEMENTSENV_BASE}/lib32 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${ELEMENTSENV_BASE}/lib32:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${ELEMENTSENV_BASE}/lib32
        fi
      fi
    fi
    if [[ -d ${ELEMENTSENV_BASE}/lib ]]; then
      if [[ -n "$LD_LIBRARY_PATH" ]]; then
        export LD_LIBRARY_PATH=${ELEMENTSENV_BASE}/lib:${LD_LIBRARY_PATH}
      else
        export LD_LIBRARY_PATH=${ELEMENTSENV_BASE}/lib
      fi
    fi
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${ELEMENTSENV_BASE}/lib64 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${ELEMENTSENV_BASE}/lib64:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${ELEMENTSENV_BASE}/lib64
        fi
      fi
    fi

    my_python_base=$(python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${ELEMENTSENV_BASE}'))")
    if [[ -d ${my_python_base} ]]; then
      if [[ -n "$PYTHONPATH" ]]; then
        export PYTHONPATH=${my_python_base}:${PYTHONPATH}
      else
        export PYTHONPATH=${my_python_base}
      fi
    else
      if [[ -d ${ELEMENTSENV_BASE}/python ]]; then
        if [[ -n "$PYTHONPATH" ]]; then
          export PYTHONPATH=${ELEMENTSENV_BASE}/python:${PYTHONPATH}
        else
          export PYTHONPATH=${ELEMENTSENV_BASE}/python
        fi
      fi
    fi
    unset my_python_base
    
    if [[ -n "$CMAKE_PREFIX_PATH" ]]; then
      export CMAKE_PREFIX_PATH=${ELEMENTSENV_BASE}:${CMAKE_PREFIX_PATH}
    else
      export CMAKE_PREFIX_PATH=${ELEMENTSENV_BASE}
    fi
    if [[ -d ${ELEMENTSENV_BASE}/cmake ]]; then
      export CMAKE_PREFIX_PATH=${ELEMENTSENV_BASE}/cmake:${CMAKE_PREFIX_PATH}
    fi
    
  fi
fi

# prepend path entries from the current install prefix to the environment
if [[ "${ELEMENTSENV_USE_PREFIX}" == "yes" ]]; then
 if [[ -d ${my_own_exe_prefix0} ]]; then

    if [[ -d ${my_own_exe_prefix0}/bin ]]; then
      export PATH=${my_own_exe_prefix0}/bin:${PATH}
    fi
    if [[ -d ${my_own_exe_prefix0}/scripts ]]; then
      export PATH=${my_own_exe_prefix0}/scripts:${PATH}
    fi
    
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${my_own_exe_prefix0}/lib32 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${my_own_exe_prefix0}/lib32:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${my_own_exe_prefix0}/lib32
        fi
      fi
    fi
    if [[ -d ${my_own_exe_prefix0}/lib ]]; then
      if [[ -n "$LD_LIBRARY_PATH" ]]; then
        export LD_LIBRARY_PATH=${my_own_exe_prefix0}/lib:${LD_LIBRARY_PATH}
      else
        export LD_LIBRARY_PATH=${my_own_exe_prefix0}/lib
      fi
    fi
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${my_own_exe_prefix0}/lib64 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${my_own_exe_prefix0}/lib64:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${my_own_exe_prefix0}/lib64
        fi
      fi
    fi
    
    my_python_base=$(python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${my_own_exe_prefix0}'))")
    if [[ -d ${my_python_base} ]]; then
      if [[ -n "$PYTHONPATH" ]]; then
        export PYTHONPATH=${my_python_base}:${PYTHONPATH}
      else
        export PYTHONPATH=${my_python_base}
      fi
    else
      if [[ -d ${my_own_exe_prefix0}/python ]]; then
        if [[ -n "$PYTHONPATH" ]]; then
          export PYTHONPATH=${my_own_exe_prefix0}/python:${PYTHONPATH}
        else
          export PYTHONPATH=${my_own_exe_prefix0}/python
        fi
      fi
    fi
    unset my_python_base
    
    if [[ -n "$CMAKE_PREFIX_PATH" ]]; then
      export CMAKE_PREFIX_PATH=${my_own_exe_prefix0}:${CMAKE_PREFIX_PATH}
    else
      export CMAKE_PREFIX_PATH=${my_own_exe_prefix0}
    fi
    if [[ -d ${ELEMENTSENV_BASE}/cmake ]]; then
      export CMAKE_PREFIX_PATH=${my_own_exe_prefix0}/cmake:${CMAKE_PREFIX_PATH}
    fi

 fi
fi

# prepend path entries from the custom install prefix to the environment
# by default it is relative to the ELEMENTSENV_BASE directory
if [[ "${ELEMENTSENV_USE_CUSTOM_PREFIX}" == "yes" ]]; then
 if [[ -d ${ELEMENTSENV_CUSTOM_PREFIX} ]]; then

    if [[ -d ${ELEMENTSENV_CUSTOM_PREFIX}/bin ]]; then
      export PATH=${ELEMENTSENV_CUSTOM_PREFIX}/bin:${PATH}
    fi
    if [[ -d ${ELEMENTSENV_CUSTOM_PREFIX}/scripts ]]; then
      export PATH=${ELEMENTSENV_CUSTOM_PREFIX}/scripts:${PATH}
    fi
    
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${ELEMENTSENV_CUSTOM_PREFIX}/lib32 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${ELEMENTSENV_CUSTOM_PREFIX}/lib32:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${ELEMENTSENV_CUSTOM_PREFIX}/lib32
        fi
      fi
    fi
    if [[ -d ${ELEMENTSENV_CUSTOM_PREFIX}/lib ]]; then
      if [[ -n "$LD_LIBRARY_PATH" ]]; then
        export LD_LIBRARY_PATH=${ELEMENTSENV_CUSTOM_PREFIX}/lib:${LD_LIBRARY_PATH}
      else
        export LD_LIBRARY_PATH=${ELEMENTSENV_CUSTOM_PREFIX}/lib
      fi
    fi
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${ELEMENTSENV_CUSTOM_PREFIX}/lib64 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${ELEMENTSENV_CUSTOM_PREFIX}/lib64:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${ELEMENTSENV_CUSTOM_PREFIX}/lib64
        fi
      fi
    fi

    my_python_base=$(python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${ELEMENTSENV_CUSTOM_PREFIX}'))")
    if [[ -d ${my_python_base} ]]; then
      if [[ -n "$PYTHONPATH" ]]; then
        export PYTHONPATH=${my_python_base}:${PYTHONPATH}
      else
        export PYTHONPATH=${my_python_base}
      fi
    else
      if [[ -d ${ELEMENTSENV_CUSTOM_PREFIX}/python ]]; then
        if [[ -n "$PYTHONPATH" ]]; then
          export PYTHONPATH=${ELEMENTSENV_CUSTOM_PREFIX}/python:${PYTHONPATH}
        else
          export PYTHONPATH=${ELEMENTSENV_CUSTOM_PREFIX}/python
        fi
      fi
    fi
    unset my_python_base
    
    if [[ -n "$CMAKE_PREFIX_PATH" ]]; then
      export CMAKE_PREFIX_PATH=${ELEMENTSENV_CUSTOM_PREFIX}:${CMAKE_PREFIX_PATH}
    else
      export CMAKE_PREFIX_PATH=${ELEMENTSENV_CUSTOM_PREFIX}
    fi
    if [[ -d ${ELEMENTSENV_BASE}/cmake ]]; then
      export CMAKE_PREFIX_PATH=${ELEMENTSENV_CUSTOM_PREFIX}/cmake:${CMAKE_PREFIX_PATH}
    fi

 fi
fi


unset arch_type

export ELEMENTSENV_CONFIG_FILE=${elementsenv_config_file_current}

fi

unset elementsenv_config_file_current

export ELEMENTSENV_CONFIG_SCRIPT=${my_own_exe_prefix0}/bin/Elementsenv_config.sh

unset my_own_prefix0
unset my_own_exe_prefix0

