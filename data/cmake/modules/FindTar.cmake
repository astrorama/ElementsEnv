if (NOT TAR_FOUND)

    find_program(TAR_EXECUTABLE tar
                 HINTS ENV TAR_INSTALL_DIR
                 PATH_SUFFIXES bin)
    set(TAR_EXECUTABLE ${TAR_EXECUTABLE} CACHE STRING "")

# handle the QUIETLY and REQUIRED arguments and set TAR_FOUND to TRUE if
# all listed variables are TRUE
    INCLUDE(FindPackageHandleStandardArgs)
    FIND_PACKAGE_HANDLE_STANDARD_ARGS(Tar DEFAULT_MSG TAR_EXECUTABLE)

    mark_as_advanced(TAR_FOUND TAR_EXECUTABLE)


endif (NOT TAR_FOUND)

