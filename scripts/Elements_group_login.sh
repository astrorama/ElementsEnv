#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  my_own_prefix2="%(this_install_prefix)s"

  if [[ -r ${my_own_prefix2}/bin/Euclid_config.sh ]]; then
    confscr=${my_own_prefix2}/bin/Euclid_config.sh
  else
    confscr=`/usr/bin/which Euclid_config.sh`
  fi
  . ${confscr} "$@"
  unset confscr

  if [[ -n "$E_BANNER" ]]; then
    cat ${E_BANNER}
    rm -f ${E_BANNER}
    unset E_BANNER
  else
    
    needs_cleanup2=no
    
    if [[ -r ${my_own_prefix2}/bin/ELogin.sh ]]; then
      elogscr=${my_own_prefix2}/bin/ELogin.sh
    else
      elogscr=`/usr/bin/which ELogin.sh`
    fi    
    if [[ -e ${elogscr} ]]; then
      . ${elogscr} --quiet "$@"
      needs_cleanup2=yes
    fi

    if [[ ! -n "$EUCLID_POST_DONE" ]]; then
      if [[ -n "$EUCLID_POST_SCRIPT" ]]; then
        if [[ -r ${my_own_prefix2}/bin/${EUCLID_POST_SCRIPT}.sh ]]; then
          epostscr=${my_own_prefix2}/bin/${EUCLID_POST_SCRIPT}.sh
        else
          epostscr=`/usr/bin/which ${EUCLID_POST_SCRIPT}.sh 2> /dev/null`
        fi
        if [[ -r ${epostscr} ]]; then
          . ${epostscr} "$@"
          export EUCLID_POST_DONE=yes
          needs_cleanup2=yes
        fi
        unset epostscr
      fi
    fi

    if [[ "$needs_cleanup2" = "yes" ]]; then
      if [[ "x$E_NO_STRIP_PATH" ==  "x" ]] ; then
        if [[ -r ${my_own_prefix2}/bin/StripPath.sh ]]; then
          stripscr=${my_own_prefix2}/bin/StripPath.sh
        else
          stripscr=`/usr/bin/which StripPath.sh 2> /dev/null`
        fi
        . ${stripscr}
        unset stripscr
      fi
    fi
                            
    unset needs_cleanup2
      
  fi

  export ELOGIN_DONE=yes

  unset my_own_prefix2

fi

