StripPath_extra_args=""
if [ -n "${E_STRIP_NON_EXIST_ONLY}" ]; then
  StripPath_extra_args="--strip-non-exist-only"
fi
StripPath_tmpfile=`python%(this_python_version)s -m ElementsEnv.PathStripper ${StripPath_extra_args} --shell=sh --mktemp -e PATH -e LD_LIBRARY_PATH -e PYTHONPATH -e HPATH `
StripPathStatus="$?"
if [ "$StripPathStatus" = 0 -a -n "$StripPath_tmpfile" ]; then
  . $StripPath_tmpfile
fi
rm -f $StripPath_tmpfile
unset StripPath_tmpfile
unset StripPath_extra_args
unset E_NO_STRIP_PATH
unset E_STRIP_NON_EXIST_ONLY
