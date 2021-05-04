# main login script for the Euclid environment


set my_own_prefix = "%(this_install_prefix)s"

set python_loc = `python%(this_python_version)s -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix='$my_own_prefix'))"`

if ( -r ${python_loc}/Euclid/Login.py ) then
  set ELogin_tmpfile = `python%(this_python_version)s ${python_loc}/Euclid/Login.py --shell=csh --mktemp ${*:q}`
  set ELoginStatus = $?
else
  set ELogin_tmpfile = `python%(this_python_version)s -m Euclid.Login --shell=csh --mktemp ${*:q}`
  set ELoginStatus = $?
endif

unset python_loc

set needs_cleanup = no

if ( ! $ELoginStatus && "$ELogin_tmpfile" != "") then
if ( -r $ELogin_tmpfile ) then
    source $ELogin_tmpfile
    rm -f $ELogin_tmpfile
  else
    echo "$ELogin_tmpfile"
  endif
  set needs_cleanup = yes
endif

unset ELogin_tmpfile

if ( "$needs_cleanup" == "yes" ) then
  if (! ${?E_NO_STRIP_PATH} ) then

    if ( -r ${my_own_prefix}/bin/StripPath.csh ) then
      set stripscr=${my_own_prefix}/bin/StripPath.csh
    else
      set stripscr=`/usr/bin/which StripPath.csh`
    endif

    source ${stripscr}

    unset stripscr

  endif
endif

unset needs_cleanup
unset my_own_prefix

exit $ELoginStatus
