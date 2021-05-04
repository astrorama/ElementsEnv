if (NOT PYXB_FOUND)

    find_program(PYXBGEN_EXECUTABLE pyxbgen
                 HINTS ENV PYXB_INSTALL_DIR
                 PATH_SUFFIXES bin)
    set(PYXBGEN_EXECUTABLE ${PYXBGEN_EXECUTABLE} CACHE STRING "")

# handle the QUIETLY and REQUIRED arguments and set PYXBGEN_FOUND to TRUE if
# all listed variables are TRUE
    INCLUDE(FindPackageHandleStandardArgs)
    FIND_PACKAGE_HANDLE_STANDARD_ARGS(PyXB DEFAULT_MSG PYXBGEN_EXECUTABLE)

    mark_as_advanced(PYXB_FOUND PYXBGEN_EXECUTABLE)


endif (NOT PYXB_FOUND)

