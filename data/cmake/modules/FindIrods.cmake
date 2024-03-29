if (NOT IRODS_FOUND)

    find_program(IGET_EXECUTABLE NAMES iget
                 HINTS ENV IRODS_INSTALL_DIR IRODS_INSTALL_DIR
                 PATH_SUFFIXES bin)
    set(IGET_EXECUTABLE ${IGET_EXECUTABLE} CACHE STRING "")

    find_program(IRSYNC_EXECUTABLE NAMES irsync
                 HINTS ENV IRODS_INSTALL_DIR IRODS_INSTALL_DIR
                 PATH_SUFFIXES bin)
    set(IRSYNC_EXECUTABLE ${IRSYNC_EXECUTABLE} CACHE STRING "")


# handle the QUIETLY and REQUIRED arguments and set IRODS_FOUND to TRUE if
# all listed variables are TRUE
    INCLUDE(FindPackageHandleStandardArgs)
    FIND_PACKAGE_HANDLE_STANDARD_ARGS(Irods DEFAULT_MSG IGET_EXECUTABLE IRSYNC_EXECUTABLE)

    mark_as_advanced(IRODS_FOUND IGET_EXECUTABLE IRSYNC_EXECUTABLE)


endif (NOT IRODS_FOUND)
