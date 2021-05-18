# default file to be tested in order
# 1) $XDG_CONFIG_HOME/ElementsEnv/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/ElementsEnv/default
# 3) for f in $XDG_CONFIG_DIRS : $f/ElementsEnv/default (if XDG_CONFIG_DIRS exists)
# 4) %(this_etc_install_prefix)s/default/ElementsEnv
# 5) %(this_etc_install_prefix)s/sysconfig/elementsenv
# 6) /etc/default/ElementsEnv
# 7) /etc/sysconfig/elementsenv

set my_own_prefix0 = "%(this_etc_install_prefix)s"
set my_own_exe_prefix0 = "%(this_install_prefix)s"

if (! $?ELEMENTSENV_CONFIG_SCRIPT) then
  setenv ELEMENTSENV_CONFIG_SCRIPT ""
endif

set cfgfiles=""

if ( ! -e ${HOME}/.noElementsEnvUserConfig ) then
  if ( $?XDG_CONFIG_HOME ) then
    set cfgfiles="$cfgfiles $XDG_CONFIG_HOME/ElementsEnv/default"
  endif
  if ( $?HOME ) then
    set cfgfiles="$cfgfiles $HOME/.config/ElementsEnv/default"
  endif
endif

if ( $?XDG_CONFIG_DIRS ) then
  foreach d (`echo $XDG_CONFIG_DIRS | tr -s ':' ' ' `)
    set cfgfiles="$cfgfiles $d/ElementsEnv/default"
  end
  unset d
endif
set cfgfiles="$cfgfiles $my_own_prefix0/default/ElementsEnv"
set cfgfiles="$cfgfiles $my_own_prefix0/sysconfig/elementsenv"
set cfgfiles="$cfgfiles /etc/default/ElementsEnv"
set cfgfiles="$cfgfiles /etc/sysconfig/elementsenv"

set elementsenv_config_file_current=""
foreach c ( $cfgfiles )
  if ( -r $c ) then
    set elementsenv_config_file_current=$c
    break
  endif
end

unset c
unset cfgfiles

if (! $?ELEMENTSENV_CONFIG_FILE) then
  setenv ELEMENTSENV_CONFIG_FILE ""
endif

if ( "${ELEMENTSENV_CONFIG_FILE}" != "${elementsenv_config_file_current}" ) then

# default values if no config file is found
setenv SOFTWARE_BASE_VAR ELEMENTSENV_BASE
setenv ELEMENTSENV_BASE %(this_elementsenv_base)s
setenv ELEMENTSENV_USE_BASE no
setenv ELEMENTSENV_USE_PREFIX no
setenv ELEMENTSENV_CUSTOM_PREFIX %(this_custom_prefix)s
setenv ELEMENTSENV_USE_CUSTOM_PREFIX no

if ( "${elementsenv_config_file_current}" != "" ) then
  eval `cat ${elementsenv_config_file_current} | sed -n -e '/^[^+]/s/\(\\\$[^ ]*\)/"\\\\\1"/' -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/setenv \1 \"\2\";/gp'`
endif

setenv ELEMENTSENV_CUSTOM_PREFIX `readlink -m ${ELEMENTSENV_CUSTOM_PREFIX}`


set arch_type=`uname -m`

# prepend path entries from the base to the environment 
if ( "${ELEMENTSENV_USE_BASE}" == "yes" ) then
  if ( -d ${ELEMENTSENV_BASE} ) then

    if ( -d ${ELEMENTSENV_BASE}/bin ) then
      setenv PATH ${ELEMENTSENV_BASE}/bin:${PATH}
    endif
    if ( -d ${ELEMENTSENV_BASE}/scripts ) then
      setenv PATH ${ELEMENTSENV_BASE}/scripts:${PATH}
    endif
    
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${ELEMENTSENV_BASE}/lib32 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_BASE}/lib32:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_BASE}/lib32        
        endif
      endif
    endif
    if ( -d ${ELEMENTSENV_BASE}/lib ) then
      if ( $?LD_LIBRARY_PATH ) then 
        setenv LD_LIBRARY_PATH ${ELEMENTSENV_BASE}/lib:${LD_LIBRARY_PATH}
      else
        setenv LD_LIBRARY_PATH ${ELEMENTSENV_BASE}/lib        
      endif
    endif
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${ELEMENTSENV_BASE}/lib64 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_BASE}/lib64:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_BASE}/lib64        
        endif
      endif
    endif
    
    set my_python_base=`python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${ELEMENTSENV_BASE}'))"`
    if ( -d ${my_python_base} ) then
      if ( $?PYTHONPATH ) then 
        setenv PYTHONPATH ${my_python_base}:${PYTHONPATH}
      else
        setenv PYTHONPATH ${my_python_base}        
      endif       
    else
      if ( -d ${ELEMENTSENV_BASE}/python ) then
        if ( $?PYTHONPATH ) then 
          setenv PYTHONPATH ${ELEMENTSENV_BASE}/python:${PYTHONPATH}
        else
          setenv PYTHONPATH ${ELEMENTSENV_BASE}/python        
        endif
      endif
    endif  
    unset my_python_base
    
    if ( $?CMAKE_PREFIX_PATH ) then 
      setenv CMAKE_PREFIX_PATH ${ELEMENTSENV_BASE}:${CMAKE_PREFIX_PATH}
    else
      setenv CMAKE_PREFIX_PATH ${ELEMENTSENV_BASE}        
    endif
    if ( -d ${ELEMENTSENV_BASE}/cmake ) then
      setenv CMAKE_PREFIX_PATH ${ELEMENTSENV_BASE}/cmake:${CMAKE_PREFIX_PATH}
    endif                
            
  endif
endif

# prepend path entries from the prefix to the environment 
if ( "${ELEMENTSENV_USE_PREFIX}" == "yes" ) then
 if ( -d ${my_own_exe_prefix0} ) then

    if ( -d ${my_own_exe_prefix0}/bin ) then
      setenv PATH ${my_own_exe_prefix0}/bin:${PATH}
    endif
    if ( -d ${my_own_exe_prefix0}/scripts ) then
      setenv PATH ${my_own_exe_prefix0}/scripts:${PATH}
    endif
    
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${my_own_exe_prefix0}/lib32 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${my_own_exe_prefix0}/lib32:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${my_own_exe_prefix0}/lib32        
        endif
      endif
    endif
    if ( -d ${my_own_exe_prefix0}/lib ) then
      if ( $?LD_LIBRARY_PATH ) then 
        setenv LD_LIBRARY_PATH ${my_own_exe_prefix0}/lib:${LD_LIBRARY_PATH}
      else
        setenv LD_LIBRARY_PATH ${my_own_exe_prefix0}/lib        
      endif
    endif
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${my_own_exe_prefix0}/lib64 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${my_own_exe_prefix0}/lib64:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${my_own_exe_prefix0}/lib64        
        endif
      endif
    endif
    
    set my_python_base=`python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${my_own_exe_prefix0}'))"`
    if ( -d ${my_python_base} ) then
      if ( $?PYTHONPATH ) then 
        setenv PYTHONPATH ${my_python_base}:${PYTHONPATH}
      else
        setenv PYTHONPATH ${my_python_base}        
      endif       
    else
      if ( -d ${my_own_exe_prefix0}/python ) then
        if ( $?PYTHONPATH ) then 
          setenv PYTHONPATH ${my_own_exe_prefix0}/python:${PYTHONPATH}
        else
          setenv PYTHONPATH ${my_own_exe_prefix0}/python        
        endif
      endif
    endif  
    unset my_python_base
    
    if ( $?CMAKE_PREFIX_PATH ) then 
      setenv CMAKE_PREFIX_PATH ${my_own_exe_prefix0}:${CMAKE_PREFIX_PATH}
    else
      setenv CMAKE_PREFIX_PATH ${my_own_exe_prefix0}        
    endif
    if ( -d ${my_own_exe_prefix0}/cmake ) then
      setenv CMAKE_PREFIX_PATH ${my_own_exe_prefix0}/cmake:${CMAKE_PREFIX_PATH}
    endif                

 endif
endif

# prepend path entries from the custom install prefix to the environment
# by default it is relative to the ELEMENTSENV_BASE directory
if ( "${ELEMENTSENV_USE_CUSTOM_PREFIX}" == "yes" ) then
 if ( -d ${ELEMENTSENV_CUSTOM_PREFIX} ) then

    if ( -d ${ELEMENTSENV_CUSTOM_PREFIX}/bin ) then
      setenv PATH ${ELEMENTSENV_CUSTOM_PREFIX}/bin:${PATH}
    endif
    if ( -d ${ELEMENTSENV_CUSTOM_PREFIX}/scripts ) then
      setenv PATH ${ELEMENTSENV_CUSTOM_PREFIX}/scripts:${PATH}
    endif
    
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${ELEMENTSENV_CUSTOM_PREFIX}/lib32 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_CUSTOM_PREFIX}/lib32:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_CUSTOM_PREFIX}/lib32        
        endif
      endif
    endif
    if ( -d ${ELEMENTSENV_CUSTOM_PREFIX}/lib ) then
      if ( $?LD_LIBRARY_PATH ) then 
        setenv LD_LIBRARY_PATH ${ELEMENTSENV_CUSTOM_PREFIX}/lib:${LD_LIBRARY_PATH}
      else
        setenv LD_LIBRARY_PATH ${ELEMENTSENV_CUSTOM_PREFIX}/lib        
      endif
    endif
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${ELEMENTSENV_CUSTOM_PREFIX}/lib64 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_CUSTOM_PREFIX}/lib64:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${ELEMENTSENV_CUSTOM_PREFIX}/lib64        
        endif
      endif
    endif
    
    set my_python_base=`python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${ELEMENTSENV_CUSTOM_PREFIX}'))"`
    if ( -d ${my_python_base} ) then
      if ( $?PYTHONPATH ) then 
        setenv PYTHONPATH ${my_python_base}:${PYTHONPATH}
      else
        setenv PYTHONPATH ${my_python_base}        
      endif       
    else
      if ( -d ${ELEMENTSENV_CUSTOM_PREFIX}/python ) then
        if ( $?PYTHONPATH ) then 
          setenv PYTHONPATH ${ELEMENTSENV_CUSTOM_PREFIX}/python:${PYTHONPATH}
        else
          setenv PYTHONPATH ${ELEMENTSENV_CUSTOM_PREFIX}/python        
        endif
      endif
    endif  
    unset my_python_base
    
    if ( $?CMAKE_PREFIX_PATH ) then 
      setenv CMAKE_PREFIX_PATH ${ELEMENTSENV_CUSTOM_PREFIX}:${CMAKE_PREFIX_PATH}
    else
      setenv CMAKE_PREFIX_PATH ${ELEMENTSENV_CUSTOM_PREFIX}        
    endif
    if ( -d ${ELEMENTSENV_CUSTOM_PREFIX}/cmake ) then
      setenv CMAKE_PREFIX_PATH ${ELEMENTSENV_CUSTOM_PREFIX}/cmake:${CMAKE_PREFIX_PATH}
    endif                

 endif
endif

unset arch_type

setenv ELEMENTSENV_CONFIG_FILE ${elementsenv_config_file_current}

endif

unset elementsenv_config_file_current

setenv ELEMENTSENV_CONFIG_SCRIPT ${my_own_exe_prefix0}/bin/ElementsEnv_config.csh

unset my_own_prefix0
unset my_own_exe_prefix0

