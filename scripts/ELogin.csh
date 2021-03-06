# main login script for the ElementsEnv environment


set my_own_prefix = "%(this_install_prefix)s"

set python_loc = `python%(this_python_version)s -c "import sys; from sysconfig import get_path; print(get_path('purelib').replace(sys.prefix, '$my_own_prefix'))"`

if ( -r ${python_loc}/ElementsEnv/Login.py ) then
  set ELogin_tmpfile = `python%(this_python_version)s ${python_loc}/ElementsEnv/Login.py --shell=csh --mktemp ${*:q}`
  set ELoginStatus = $?
else
  set ELogin_tmpfile = `python%(this_python_version)s -m ElementsEnv.Login --shell=csh --mktemp ${*:q}`
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
