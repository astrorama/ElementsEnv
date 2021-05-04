# default file to be tested in order
# 1) $XDG_CONFIG_HOME/Euclid/default (if XDG_CONFIG_HOME exists)
# 2) $HOME/.config/Euclid/default
# 3) for f in $XDG_CONFIG_DIRS : $f/Euclid/default (if XDG_CONFIG_DIRS exists)
# 4) %(this_etc_install_prefix)s/default/Euclid
# 5) %(this_etc_install_prefix)s/sysconfig/euclid
# 6) /etc/default/Euclid
# 7) /etc/sysconfig/euclid

set my_own_prefix0 = "%(this_etc_install_prefix)s"
set my_own_exe_prefix0 = "%(this_install_prefix)s"

if (! $?EUCLID_CONFIG_SCRIPT) then
  setenv EUCLID_CONFIG_SCRIPT ""
endif

set cfgfiles=""

if ( ! -e ${HOME}/.noEuclidUserConfig ) then
  if ( $?XDG_CONFIG_HOME ) then
    set cfgfiles="$cfgfiles $XDG_CONFIG_HOME/Euclid/default"
  endif
  if ( $?HOME ) then
    set cfgfiles="$cfgfiles $HOME/.config/Euclid/default"
  endif
endif

if ( $?XDG_CONFIG_DIRS ) then
  foreach d (`echo $XDG_CONFIG_DIRS | tr -s ':' ' ' `)
    set cfgfiles="$cfgfiles $d/Euclid/default"
  end
  unset d
endif
set cfgfiles="$cfgfiles $my_own_prefix0/default/Euclid"
set cfgfiles="$cfgfiles $my_own_prefix0/sysconfig/euclid"
set cfgfiles="$cfgfiles /etc/default/Euclid"
set cfgfiles="$cfgfiles /etc/sysconfig/euclid"

set euclid_config_file_current=""
foreach c ( $cfgfiles )
  if ( -r $c ) then
    set euclid_config_file_current=$c
    break
  endif
end

unset c
unset cfgfiles

if (! $?EUCLID_CONFIG_FILE) then
  setenv EUCLID_CONFIG_FILE ""
endif

if ( "${EUCLID_CONFIG_FILE}" != "${euclid_config_file_current}" ) then

# default values if no config file is found
setenv SOFTWARE_BASE_VAR EUCLID_BASE
setenv EUCLID_BASE %(this_euclid_base)s
setenv EUCLID_USE_BASE no
setenv EUCLID_USE_PREFIX no
setenv EUCLID_CUSTOM_PREFIX %(this_euclid_base)s/../../usr
setenv EUCLID_USE_CUSTOM_PREFIX no

if ( "${euclid_config_file_current}" != "" ) then
  eval `cat ${euclid_config_file_current} | sed -n -e '/^[^+]/s/\(\\\$[^ ]*\)/"\\\\\1"/' -e '/^[^+]/s/\([^=]*\)[=]\(.*\)/setenv \1 \"\2\";/gp'`
endif

setenv EUCLID_CUSTOM_PREFIX `readlink -m ${EUCLID_CUSTOM_PREFIX}`


set arch_type=`uname -m`

# prepend path entries from the base to the environment 
if ( "${EUCLID_USE_BASE}" == "yes" ) then
  if ( -d ${EUCLID_BASE} ) then

    if ( -d ${EUCLID_BASE}/bin ) then
      setenv PATH ${EUCLID_BASE}/bin:${PATH}
    endif
    if ( -d ${EUCLID_BASE}/scripts ) then
      setenv PATH ${EUCLID_BASE}/scripts:${PATH}
    endif
    
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${EUCLID_BASE}/lib32 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib32:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib32        
        endif
      endif
    endif
    if ( -d ${EUCLID_BASE}/lib ) then
      if ( $?LD_LIBRARY_PATH ) then 
        setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib:${LD_LIBRARY_PATH}
      else
        setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib        
      endif
    endif
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${EUCLID_BASE}/lib64 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib64:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${EUCLID_BASE}/lib64        
        endif
      endif
    endif
    
    set my_python_base=`python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${EUCLID_BASE}'))"`
    if ( -d ${my_python_base} ) then
      if ( $?PYTHONPATH ) then 
        setenv PYTHONPATH ${my_python_base}:${PYTHONPATH}
      else
        setenv PYTHONPATH ${my_python_base}        
      endif       
    else
      if ( -d ${EUCLID_BASE}/python ) then
        if ( $?PYTHONPATH ) then 
          setenv PYTHONPATH ${EUCLID_BASE}/python:${PYTHONPATH}
        else
          setenv PYTHONPATH ${EUCLID_BASE}/python        
        endif
      endif
    endif  
    unset my_python_base
    
    if ( $?CMAKE_PREFIX_PATH ) then 
      setenv CMAKE_PREFIX_PATH ${EUCLID_BASE}:${CMAKE_PREFIX_PATH}
    else
      setenv CMAKE_PREFIX_PATH ${EUCLID_BASE}        
    endif
    if ( -d ${EUCLID_BASE}/cmake ) then
      setenv CMAKE_PREFIX_PATH ${EUCLID_BASE}/cmake:${CMAKE_PREFIX_PATH}
    endif                
            
  endif
endif

# prepend path entries from the prefix to the environment 
if ( "${EUCLID_USE_PREFIX}" == "yes" ) then
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
# by default it is relative to the EUCLID_BASE directory
if ( "${EUCLID_USE_CUSTOM_PREFIX}" == "yes" ) then
 if ( -d ${EUCLID_CUSTOM_PREFIX} ) then

    if ( -d ${EUCLID_CUSTOM_PREFIX}/bin ) then
      setenv PATH ${EUCLID_CUSTOM_PREFIX}/bin:${PATH}
    endif
    if ( -d ${EUCLID_CUSTOM_PREFIX}/scripts ) then
      setenv PATH ${EUCLID_CUSTOM_PREFIX}/scripts:${PATH}
    endif
    
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${EUCLID_CUSTOM_PREFIX}/lib32 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${EUCLID_CUSTOM_PREFIX}/lib32:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${EUCLID_CUSTOM_PREFIX}/lib32        
        endif
      endif
    endif
    if ( -d ${EUCLID_CUSTOM_PREFIX}/lib ) then
      if ( $?LD_LIBRARY_PATH ) then 
        setenv LD_LIBRARY_PATH ${EUCLID_CUSTOM_PREFIX}/lib:${LD_LIBRARY_PATH}
      else
        setenv LD_LIBRARY_PATH ${EUCLID_CUSTOM_PREFIX}/lib        
      endif
    endif
    if ( "${arch_type}" == "x86_64" ) then
      if ( -d ${EUCLID_CUSTOM_PREFIX}/lib64 ) then
        if ( $?LD_LIBRARY_PATH ) then 
          setenv LD_LIBRARY_PATH ${EUCLID_CUSTOM_PREFIX}/lib64:${LD_LIBRARY_PATH}
        else
          setenv LD_LIBRARY_PATH ${EUCLID_CUSTOM_PREFIX}/lib64        
        endif
      endif
    endif
    
    set my_python_base=`python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='${EUCLID_CUSTOM_PREFIX}'))"`
    if ( -d ${my_python_base} ) then
      if ( $?PYTHONPATH ) then 
        setenv PYTHONPATH ${my_python_base}:${PYTHONPATH}
      else
        setenv PYTHONPATH ${my_python_base}        
      endif       
    else
      if ( -d ${EUCLID_CUSTOM_PREFIX}/python ) then
        if ( $?PYTHONPATH ) then 
          setenv PYTHONPATH ${EUCLID_CUSTOM_PREFIX}/python:${PYTHONPATH}
        else
          setenv PYTHONPATH ${EUCLID_CUSTOM_PREFIX}/python        
        endif
      endif
    endif  
    unset my_python_base
    
    if ( $?CMAKE_PREFIX_PATH ) then 
      setenv CMAKE_PREFIX_PATH ${EUCLID_CUSTOM_PREFIX}:${CMAKE_PREFIX_PATH}
    else
      setenv CMAKE_PREFIX_PATH ${EUCLID_CUSTOM_PREFIX}        
    endif
    if ( -d ${EUCLID_CUSTOM_PREFIX}/cmake ) then
      setenv CMAKE_PREFIX_PATH ${EUCLID_CUSTOM_PREFIX}/cmake:${CMAKE_PREFIX_PATH}
    endif                

 endif
endif

unset arch_type

setenv EUCLID_CONFIG_FILE ${euclid_config_file_current}

endif

unset euclid_config_file_current

setenv EUCLID_CONFIG_SCRIPT ${my_own_exe_prefix0}/bin/Euclid_config.csh

unset my_own_prefix0
unset my_own_exe_prefix0

