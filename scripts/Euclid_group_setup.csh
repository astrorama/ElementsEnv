#!/bin/csh
if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  set my_own_prefix3 = "%(this_install_prefix)s"

  if ( -r ${my_own_prefix3}/bin/Euclid_config.csh ) then
    set confscr=${my_own_prefix3}/bin/Euclid_config.csh
  else
    set confscr=`/usr/bin/which Euclid_config.csh`        
  endif
  source ${confscr} "${*:q}" >& /dev/null
  unset confscr    

  if ( -r ${my_own_prefix3}/bin/ELogin.csh ) then
    set elogscr=${my_own_prefix3}/bin/ELogin.csh
  else
    set elogscr=`/usr/bin/which ELogin.csh`        
  endif
  if ( -e ${elogscr} ) then
    
    set needs_cleanup3=no
    
    if ( $?ELOGIN_DONE ) then
      source ${elogscr} --shell-only --silent ${*:q} >& /dev/null
    else
      
      setenv E_BANNER `mktemp`
      source ${elogscr} --quiet ${*:q} >! ${E_BANNER}

      if ( ! $?EUCLID_POST_DONE ) then
        if ( $?EUCLID_POST_SCRIPT ) then
          if ( -r "${my_own_prefix3}/bin/${EUCLID_POST_SCRIPT}.csh" ) then
            set epostscr=${my_own_prefix3}/bin/${EUCLID_POST_SCRIPT}.csh
          else
            if ( -X ${EUCLID_POST_SCRIPT}.csh ) then
              set epostscr=`/usr/bin/which ${EUCLID_POST_SCRIPT}.csh`
            else
              set epostscr=""
            endif        
          endif
          if ( -r "${epostscr}" ) then
            source ${epostscr} ${*:q} >>! ${E_BANNER}
            setenv EUCLID_POST_DONE yes
            set needs_cleanup3=yes
          endif
          unset epostscr
        endif
      endif
      
    endif
    
    if ( "$needs_cleanup3" == "yes" ) then
      if (! ${?E_NO_STRIP_PATH} ) then
        if ( -r ${my_own_prefix3}/bin/StripPath.csh ) then
          set stripscr=${my_own_prefix3}/bin/StripPath.csh
        else
          set stripscr=`/usr/bin/which StripPath.csh`        
        endif
        source ${stripscr}
        unset stripscr
      endif
    endif
        
    unset needs_cleanup3
    
    
  endif
  unset elogscr


  unset my_own_prefix3

endif

