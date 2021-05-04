
if ( shopt -q login_shell || [[ -o login ]] ) ; then
  if [ -O /tmp/$USER -a -d /tmp/$USER ]; then
    TMPDIR=/tmp/$USER
  else
    # You may wish to remove this line, it is there in case
    # a user has put a file 'tmp' in there directory or a
    rm -rf /tmp/$USER 2> /dev/null
    mkdir -p /tmp/$USER
    TMPDIR=/tmp/$USER
  fi

  TMP=$TMPDIR
  TEMP=$TMPDIR

  export TMPDIR TMP TEMP

fi

