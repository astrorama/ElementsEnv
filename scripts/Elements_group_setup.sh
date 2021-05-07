#!/bin/sh
if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  my_own_prefix3="%(this_install_prefix)s"

  if [[ -r ${my_own_prefix3}/bin/Euclid_config.sh ]]; then
    confscr=${my_own_prefix3}/bin/Euclid_config.sh
  else
    confscr=`/usr/bin/which Euclid_config.sh`
  fi
  . ${confscr} "$@" > /dev/null 2>&1
  unset confscr

  if [[ -r ${my_own_prefix3}/bin/ELogin.sh ]]; then
    elogscr=${my_own_prefix3}/bin/ELogin.sh
  else
    elogscr=`/usr/bin/which ELogin.sh`
  fi    
  if [[ -e ${elogscr} ]]; then
  
    needs_cleanup3=no
  
    if [[ -n "$ELOGIN_DONE" ]]; then
      # The login part has already been done. Only the shell (setup) part is redone.
      # This is mandatory for the creation of a subshell.
      . ${elogscr} --shell-only --silent "$@" > /dev/null 2>&1
    else
      # The full login and setup is not performed.
      export E_BANNER=`mktemp`
      . ${elogscr} --quiet "$@" >> ${E_BANNER}
      
      if [[ ! -n "$EUCLID_POST_DONE" ]]; then
        if [[ -n "$EUCLID_POST_SCRIPT" ]]; then
          if [[ -r ${my_own_prefix3}/bin/${EUCLID_POST_SCRIPT}.sh ]]; then
            epostscr=${my_own_prefix3}/bin/${EUCLID_POST_SCRIPT}.sh
          else
            epostscr=`/usr/bin/which ${EUCLID_POST_SCRIPT}.sh 2> /dev/null`
          fi
          if [[ -r ${epostscr} ]]; then
            . ${epostscr} "$@" >> ${E_BANNER}
            export EUCLID_POST_DONE=yes
            needs_cleanup3=yes
          fi
          unset epostscr
        fi
      fi
                
    fi
    
    if [[ "$needs_cleanup3" = "yes" ]]; then
      if [[ "x$E_NO_STRIP_PATH" ==  "x" ]] ; then
        if [[ -r ${my_own_prefix3}/bin/StripPath.sh ]]; then
          stripscr=${my_own_prefix3}/bin/StripPath.sh
        else
          stripscr=`/usr/bin/which StripPath.sh 2> /dev/null`
        fi
        . ${stripscr}
        unset stripscr
      fi
    fi    
    
    unset needs_cleanup3
    
  fi
  unset elogscr
    
  unset my_own_prefix3

fi

