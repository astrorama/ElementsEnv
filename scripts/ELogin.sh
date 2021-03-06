# main login script for the ElementsEnv environment

my_own_prefix="%(this_install_prefix)s"

python_loc=`python%(this_python_version)s -c "import sys; from sysconfig import get_path; print(get_path('purelib').replace(sys.prefix, '$my_own_prefix'))"`

if [[ -r ${python_loc}/ElementsEnv/Login.py ]]; then
  ELogin_tmpfile=`python%(this_python_version)s ${python_loc}/ElementsEnv/Login.py --shell=sh --mktemp "$@"`
  ELoginStatus="$?"
else
  ELogin_tmpfile=`python%(this_python_version)s -m ElementsEnv.Login --shell=sh --mktemp "$@"`
  ELoginStatus="$?"
fi

unset python_loc

needs_cleanup=no

if [[ "$ELoginStatus" = 0 && -n "$ELogin_tmpfile" ]]; then
  if [[ -r $ELogin_tmpfile ]]; then
    . $ELogin_tmpfile
    rm -f $ELogin_tmpfile
  else
    echo "$ELogin_tmpfile"
  fi
  needs_cleanup=yes
fi

unset ELogin_tmpfile

if [[ "$needs_cleanup" = "yes" ]]; then
  if [[ "x$E_NO_STRIP_PATH" ==  "x" ]] ; then

    if [[ -r ${my_own_prefix}/bin/StripPath.sh ]]; then
      stripscr=${my_own_prefix}/bin/StripPath.sh
    else
      stripscr=`/usr/bin/which StripPath.sh`
    fi
    . ${stripscr}

    unset stripscr

  fi
fi

unset needs_cleanup
unset my_own_prefix

$(exit $ELoginStatus)
