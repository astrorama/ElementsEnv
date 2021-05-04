if (NOT SPHINX_FOUND)

  find_package(PythonInterp ${PYTHON_EXPLICIT_VERSION})

  # ----------------------------------------------------------------------------
  # default components to look for
  if (NOT Sphinx_FIND_COMPONENTS)
    set (Sphinx_FIND_COMPONENTS "build" "apidoc")
  else()
    foreach (_sphinx_tool IN LISTS Sphinx_FIND_COMPONENTS)
      if(NOT _sphinx_tool MATCHES "^(build|apidoc)$")
        message (FATAL_ERROR "Invalid Sphinx component ${_sphinx_tool}")
      endif()
    endforeach()
  endif ()


# ----------------------------------------------------------------------------
# find components, i.e., build tools
  foreach (_sphinx_tool IN LISTS Sphinx_FIND_COMPONENTS)
    string(TOUPPER ${_sphinx_tool} _SPHINX_TOOL_UPPER)
    set(explicit_sphinx)
    set(implicit_sphinx sphinx-${_sphinx_tool})
    if(PYTHON_EXPLICIT_VERSION)
      set(explicit_sphinx sphinx-${_sphinx_tool}-${PYTHON_EXPLICIT_VERSION})
    else()
      set(explicit_sphinx sphinx-${_sphinx_tool})
    endif()
    find_program (
      SPHINX_${_SPHINX_TOOL_UPPER}_EXECUTABLE
      NAMES ${explicit_sphinx} ${explicit_sphinx}.py ${implicit_sphinx} ${implicit_sphinx}
      HINTS ENV SPHINX_INSTALL_DIR
      PATH_SUFFIXES bin
      DOC   "The sphinx-${_sphinx_tool} Python script."
    )
    set(Sphinx_${_sphinx_tool}_FOUND TRUE) # for the HANDLE_COMPONENTS
	set(SPHINX_${_SPHINX_TOOL_UPPER}_EXECUTABLE ${SPHINX_${_SPHINX_TOOL_UPPER}_EXECUTABLE} CACHE STRING "")
    mark_as_advanced (SPHINX_${_SPHINX_TOOL_UPPER}_EXECUTABLE)
    list (APPEND _SPHINX_REQUIRED_VARS SPHINX_${_SPHINX_TOOL_UPPER}_EXECUTABLE)
  endforeach ()

  unset(_sphinx_tool)
  unset(_SPHINX_TOOL_UPPER)

# handle the QUIETLY and REQUIRED arguments and set SPHINX_FOUND to TRUE if
# all listed variables are TRUE
  INCLUDE(FindPackageHandleStandardArgs)
  FIND_PACKAGE_HANDLE_STANDARD_ARGS(Sphinx REQUIRED_VARS ${_SPHINX_REQUIRED_VARS} HANDLE_COMPONENTS)

  mark_as_advanced(SPHINX_FOUND)

  unset(_SPHINX_REQUIRED_VARS)

endif (NOT SPHINX_FOUND)

