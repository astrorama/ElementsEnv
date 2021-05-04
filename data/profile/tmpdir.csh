if ( $?loginsh ) then
  
  if ( -o /tmp/$USER && -d /tmp/$USER ) then
    setenv TMPDIR /tmp/$USER
  else
    rm -rf /tmp/$USER >& /dev/null
    mkdir -p /tmp/$USER
    setenv TMPDIR /tmp/$USER  
  endif

  setenv TMP $TMPDIR
  setenv TEMP $TMPDIR  
    
endif
