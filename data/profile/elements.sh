if [[ ! ( "%(this_install_prefix)s" = "/usr" && ( -e /etc/sysconfig/noEuclidDefaultProfile || -e ${HOME}/.noEuclidDefaultProfile ) ) ]]; then

if [[ ! -e ${HOME}/.noEuclidLoginScript ]]; then

  my_own_prefix4="%(this_install_prefix)s"


  if [[ -r ${my_own_prefix4}/bin/Euclid_config.sh ]]; then
    confscr=${my_own_prefix4}/bin/Euclid_config.sh
  else
    confscr=`/usr/bin/which Euclid_config.sh`
  fi
  . ${confscr} "$@"
  unset confscr

  # shell part. has to deal with the shell settings. Pretty much everything but 
  # the environment variables. The script can be manually called from .bashrc
  if [[ -r ${my_own_prefix4}/bin/Euclid_group_setup.sh ]]; then
    shellscr=${my_own_prefix4}/bin/Euclid_group_setup.sh
  else
    shellscr=`/usr/bin/which Euclid_group_setup.sh`
  fi
  if  [[ -e ${shellscr} ]]; then
     . ${shellscr} "$@"
  fi
  unset shellscr

  # login part. has to deal with the environment. The script can be called manually from 
  # .bash_profile
  if ( (shopt -q login_shell || [[ -o login ]]) && ( [[ $- == *i* ]] || -o interactive) ) 2> /dev/null ; then
    if [[ -r ${my_own_prefix4}/bin/Euclid_group_login.sh ]]; then
      loginscr=${my_own_prefix4}/bin/Euclid_group_login.sh
    else
      loginscr=`/usr/bin/which Euclid_group_login.sh`
    fi
    if [[ -e ${loginscr} ]]; then
       . ${loginscr} "$@"
    fi
    unset loginscr
  fi

  if [[ -n "$E_BANNER" ]]; then
    rm -f ${E_BANNER}
    unset E_BANNER
  fi

  unset my_own_prefix4

fi

fi
