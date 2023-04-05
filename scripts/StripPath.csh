set StripPath_extra_args = ""
if ( "${E_STRIP_NON_EXIST_ONLY}" != "" ) then
  set StripPath_extra_args = "--strip-non-exist-only"
endif
set StripPath_tmpfile = `python%(this_python_version)s -m ElementsEnv.PathStripper ${StripPath_extra_args} --shell=csh --mktemp -e PATH -e LD_LIBRARY_PATH -e PYTHONPATH -e HPATH `
set StripPathStatus = $?
if ( ! $StripPathStatus && "$StripPath_tmpfile" != "" ) then
  source $StripPath_tmpfile
endif
rm -f $StripPath_tmpfile
unset StripPath_tmpfile
unset StripPath_extra_args
unsetenv E_NO_STRIP_PATH
unsetenv E_STRIP_NON_EXIST_ONLY
