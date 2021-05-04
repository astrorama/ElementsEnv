#!/bin/csh
if ( ! -e ${HOME}/.noEuclidLoginScript ) then

  set my_own_prefix2 = "%(this_install_prefix)s"

  if ( -r ${my_own_prefix2}/bin/Euclid_config.csh ) then
    set confscr=${my_own_prefix2}/bin/Euclid_config.csh
  else
    set confscr=`/usr/bin/which Euclid_config.csh`        
  endif
  source ${confscr} "${*:q}"
  unset confscr    

  if ( $?E_BANNER ) then
    cat ${E_BANNER}
    rm -f ${E_BANNER}
    unsetenv E_BANNER
  else

    set needs_cleanup2=no

    if ( -r ${my_own_prefix2}/bin/ELogin.csh ) then
      set elogscr=${my_own_prefix2}/bin/ELogin.csh
    else
      set elogscr=`/usr/bin/which ELogin.csh`        
    endif
    if ( -e ${elogscr} ) then
      source ${elogscr} --quiet ${*:q}
      set needs_cleanup2=yes
    endif

    if ( ! $?EUCLID_POST_DONE ) then
      if ( $?EUCLID_POST_SCRIPT ) then
        if ( -r "${my_own_prefix2}/bin/${EUCLID_POST_SCRIPT}.csh" ) then
          set epostscr=${my_own_prefix2}/bin/${EUCLID_POST_SCRIPT}.csh
        else
          if ( -X ${EUCLID_POST_SCRIPT}.csh ) then
            set epostscr=`/usr/bin/which ${EUCLID_POST_SCRIPT}.csh`
          else
            set epostscr=""
          endif        
        endif
        if ( -r "${epostscr}" ) then
          source ${epostscr} ${*:q}
          setenv EUCLID_POST_DONE yes
          set needs_cleanup2=yes
        endif
        unset epostscr
      endif
    endif
  
    if ( "$needs_cleanup2" == "yes" ) then
      if (! ${?E_NO_STRIP_PATH} ) then
        if ( -r ${my_own_prefix2}/bin/StripPath.csh ) then
          set stripscr=${my_own_prefix2}/bin/StripPath.csh
        else
          set stripscr=`/usr/bin/which StripPath.csh`        
        endif
        source ${stripscr}
        unset stripscr
      endif
    endif
        
    unset needs_cleanup2
  
  endif

                            
  setenv ELOGIN_DONE yes

  unset my_own_prefix2

endif

