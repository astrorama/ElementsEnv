# default file to be tested in order
# 1) $XDG_CONFIG_HOME/Euclid/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/Euclid/default
# 3) for f in $XDG_CONFIG_DIRS : $f/Euclid/default
# 4) %(this_etc_install_prefix)s/default/Euclid
# 5) %(this_etc_install_prefix)s/sysconfig/euclid
# 6) /etc/default/Euclid
# 7) /etc/sysconfig/euclid

my_own_prefix0="%(this_etc_install_prefix)s"
my_own_exe_prefix0="%(this_install_prefix)s"

cfgfiles=""

if [[ ! -e ${HOME}/.noEuclidUserConfig ]]; then
  if [[  -n "$XDG_CONFIG_HOME" ]]; then
    cfgfiles="$cfgfiles $XDG_CONFIG_HOME/Euclid/default"
  fi
  if [[ -n "$HOME" ]]; then
    cfgfiles="$cfgfiles $HOME/.config/Euclid/default"
  fi
fi

if [[ -n "$XDG_CONFIG_DIRS" ]]; then
  for d in $(echo $XDG_CONFIG_DIRS | tr -s ':' ' ')
  do
    cfgfiles="$cfgfiles $d/Euclid/default"
  done
  unset d
fi
cfgfiles="$cfgfiles $my_own_prefix0/default/Euclid"
cfgfiles="$cfgfiles $my_own_prefix0/sysconfig/euclid"
cfgfiles="$cfgfiles /etc/default/Euclid"
cfgfiles="$cfgfiles /etc/sysconfig/euclid"

euclid_config_file_current=""
for c in $(echo $cfgfiles)
do
  if [[ -r $c ]]; then
    euclid_config_file_current=$c
    break;
  fi
done

unset c
unset cfgfiles

if [[ ! "${EUCLID_CONFIG_FILE}" = "${euclid_config_file_current}" ]]; then

# default values if no config file is found
export SOFTWARE_BASE_VAR=EUCLID_BASE
export EUCLID_BASE=%(this_euclid_base)s
export EUCLID_USE_BASE=no
export EUCLID_USE_PREFIX=no
export EUCLID_CUSTOM_PREFIX=%(this_euclid_base)s/../../usr
export EUCLID_USE_CUSTOM_PREFIX=no

if [[ -n "${euclid_config_file_current}" ]]; then
  eval `cat ${euclid_config_file_current} | sed -n -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/\1="\2"; export \1;/gp'`
fi

export EUCLID_CUSTOM_PREFIX=$(readlink -m ${EUCLID_CUSTOM_PREFIX})

arch_type=`uname -m`

# prepend path entries from the base to the environment
if [[ "${EUCLID_USE_BASE}" == "yes" ]]; then
  if [[ -d ${EUCLID_BASE} ]]; then
    
    if [[ -d ${EUCLID_BASE}/bin ]]; then
      export PATH=${EUCLID_BASE}/bin:${PATH}
    fi
    if [[ -d ${EUCLID_BASE}/scripts ]]; then
      export PATH=${EUCLID_BASE}/scripts:${PATH}
    fi
    
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${EUCLID_BASE}/lib32 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib32:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib32
        fi
      fi
    fi
    if [[ -d ${EUCLID_BASE}/lib ]]; then
      if [[ -n "$LD_LIBRARY_PATH" ]]; then
        export LD_LIBRARY_PATH=${EUCLID_BASE}/lib:${LD_LIBRARY_PATH}
      else
        export LD_LIBRARY_PATH=${EUCLID_BASE}/lib
      fi
    fi
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${EUCLID_BASE}/lib64 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib64:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${EUCLID_BASE}/lib64
        fi
      fi
    fi

    my_python_base=$(python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${EUCLID_BASE}'))")
    if [[ -d ${my_python_base} ]]; then
      if [[ -n "$PYTHONPATH" ]]; then
        export PYTHONPATH=${my_python_base}:${PYTHONPATH}
      else
        export PYTHONPATH=${my_python_base}
      fi
    else
      if [[ -d ${EUCLID_BASE}/python ]]; then
        if [[ -n "$PYTHONPATH" ]]; then
          export PYTHONPATH=${EUCLID_BASE}/python:${PYTHONPATH}
        else
          export PYTHONPATH=${EUCLID_BASE}/python
        fi
      fi
    fi
    unset my_python_base
    
    if [[ -n "$CMAKE_PREFIX_PATH" ]]; then
      export CMAKE_PREFIX_PATH=${EUCLID_BASE}:${CMAKE_PREFIX_PATH}
    else
      export CMAKE_PREFIX_PATH=${EUCLID_BASE}
    fi
    if [[ -d ${EUCLID_BASE}/cmake ]]; then
      export CMAKE_PREFIX_PATH=${EUCLID_BASE}/cmake:${CMAKE_PREFIX_PATH}
    fi
    
  fi
fi

# prepend path entries from the current install prefix to the environment
if [[ "${EUCLID_USE_PREFIX}" == "yes" ]]; then
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
    if [[ -d ${EUCLID_BASE}/cmake ]]; then
      export CMAKE_PREFIX_PATH=${my_own_exe_prefix0}/cmake:${CMAKE_PREFIX_PATH}
    fi

 fi
fi

# prepend path entries from the custom install prefix to the environment
# by default it is relative to the EUCLID_BASE directory
if [[ "${EUCLID_USE_CUSTOM_PREFIX}" == "yes" ]]; then
 if [[ -d ${EUCLID_CUSTOM_PREFIX} ]]; then

    if [[ -d ${EUCLID_CUSTOM_PREFIX}/bin ]]; then
      export PATH=${EUCLID_CUSTOM_PREFIX}/bin:${PATH}
    fi
    if [[ -d ${EUCLID_CUSTOM_PREFIX}/scripts ]]; then
      export PATH=${EUCLID_CUSTOM_PREFIX}/scripts:${PATH}
    fi
    
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${EUCLID_CUSTOM_PREFIX}/lib32 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${EUCLID_CUSTOM_PREFIX}/lib32:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${EUCLID_CUSTOM_PREFIX}/lib32
        fi
      fi
    fi
    if [[ -d ${EUCLID_CUSTOM_PREFIX}/lib ]]; then
      if [[ -n "$LD_LIBRARY_PATH" ]]; then
        export LD_LIBRARY_PATH=${EUCLID_CUSTOM_PREFIX}/lib:${LD_LIBRARY_PATH}
      else
        export LD_LIBRARY_PATH=${EUCLID_CUSTOM_PREFIX}/lib
      fi
    fi
    if [[ "${arch_type}" == "x86_64" ]]; then
      if [[ -d ${EUCLID_CUSTOM_PREFIX}/lib64 ]]; then
        if [[ -n "$LD_LIBRARY_PATH" ]]; then
          export LD_LIBRARY_PATH=${EUCLID_CUSTOM_PREFIX}/lib64:${LD_LIBRARY_PATH}
        else
          export LD_LIBRARY_PATH=${EUCLID_CUSTOM_PREFIX}/lib64
        fi
      fi
    fi

    my_python_base=$(python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${EUCLID_CUSTOM_PREFIX}'))")
    if [[ -d ${my_python_base} ]]; then
      if [[ -n "$PYTHONPATH" ]]; then
        export PYTHONPATH=${my_python_base}:${PYTHONPATH}
      else
        export PYTHONPATH=${my_python_base}
      fi
    else
      if [[ -d ${EUCLID_CUSTOM_PREFIX}/python ]]; then
        if [[ -n "$PYTHONPATH" ]]; then
          export PYTHONPATH=${EUCLID_CUSTOM_PREFIX}/python:${PYTHONPATH}
        else
          export PYTHONPATH=${EUCLID_CUSTOM_PREFIX}/python
        fi
      fi
    fi
    unset my_python_base
    
    if [[ -n "$CMAKE_PREFIX_PATH" ]]; then
      export CMAKE_PREFIX_PATH=${EUCLID_CUSTOM_PREFIX}:${CMAKE_PREFIX_PATH}
    else
      export CMAKE_PREFIX_PATH=${EUCLID_CUSTOM_PREFIX}
    fi
    if [[ -d ${EUCLID_BASE}/cmake ]]; then
      export CMAKE_PREFIX_PATH=${EUCLID_CUSTOM_PREFIX}/cmake:${CMAKE_PREFIX_PATH}
    fi

 fi
fi


unset arch_type

export EUCLID_CONFIG_FILE=${euclid_config_file_current}

fi

unset euclid_config_file_current

export EUCLID_CONFIG_SCRIPT=${my_own_exe_prefix0}/bin/Euclid_config.sh

unset my_own_prefix0
unset my_own_exe_prefix0

