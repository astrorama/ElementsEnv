# -*- cmake -*-
#
# - Find tools needed for building RPM Packages
#   on Linux systems and defines macro that helps to
#   build source or binary RPM, the MACRO assumes
#   CMake 2.4.x which includes CPack support.
#   CPack is used to build tar.gz source tarball
#   which may be used by a custom user-made spec file.
#
# - Define ADD_RPM_TARGETS which defines
#   two (top-level) CUSTOM targets for building
#   source and binary RPMs
#
# Those CMake macros are provided by the TSP Developer Team
# https://savannah.nongnu.org/projects/tsp
#

IF (UNIX)

  if(NOT RPMBUILD_FOUND)

  # Look for RPM builder executable
  FIND_PROGRAM(RPMBUILD_EXECUTABLE
    NAMES rpmbuild
    PATHS "/usr/bin;/usr/lib/rpm"
    PATH_SUFFIXES bin
    DOC "The RPM builder tool")

  execute_process(COMMAND ${RPMBUILD_EXECUTABLE} --version
    OUTPUT_VARIABLE RPMBUILD_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE)

  string(REGEX REPLACE "^(.*\n)?RPM version ([.0-9]+).*"
    "\\2" RPMBUILD_VERSION "${RPMBUILD_VERSION}")

# handle the QUIETLY and REQUIRED arguments and set CCFITS_FOUND to TRUE if
# all listed variables are TRUE
  INCLUDE(FindPackageHandleStandardArgs)
  FIND_PACKAGE_HANDLE_STANDARD_ARGS(RPMBuild DEFAULT_MSG RPMBUILD_EXECUTABLE RPMBUILD_VERSION)

  mark_as_advanced(RPMBUILD_FOUND RPMBUILD_EXECUTABLE RPMBUILD_VERSION)

  IF (RPMBUILD_FOUND)
    #
    # - first arg  (ARGV0) is RPM name
    # - second arg (ARGV1) is the RPM spec file path [optional]
    # - third arg  (ARGV2) is the RPM ROOT DIRECTORY used to build RPMs [optional]
    #
    MACRO(ADD_RPM_TARGETS RPMNAME)

      #
      # If no spec file is provided create a minimal one
      #
      IF ("${ARGV1}" STREQUAL "")
        SET(SPECFILE_PATH "${CMAKE_BINARY_DIR}/${RPMNAME}.spec")
      ELSE ("${ARGV1}" STREQUAL "")
        SET(SPECFILE_PATH "${ARGV1}")
      ENDIF("${ARGV1}" STREQUAL "")

      # Verify whether if RPM_ROOTDIR was provided or not
      IF("${ARGV2}" STREQUAL "")
        SET(RPM_ROOTDIR ${CMAKE_BINARY_DIR}/RPM)
      ELSE ("${ARGV2}" STREQUAL "")
        SET(RPM_ROOTDIR "${ARGV2}")
      ENDIF("${ARGV2}" STREQUAL "")
      MESSAGE(STATUS "RPM Build:: Using RPM_ROOTDIR=${RPM_ROOTDIR}")

      # Prepare RPM build tree
      FILE(MAKE_DIRECTORY ${RPM_ROOTDIR})
      FILE(MAKE_DIRECTORY ${RPM_ROOTDIR}/tmp)
      FILE(MAKE_DIRECTORY ${RPM_ROOTDIR}/BUILD)
      FILE(MAKE_DIRECTORY ${RPM_ROOTDIR}/RPMS)
      FILE(MAKE_DIRECTORY ${RPM_ROOTDIR}/SOURCES)
      FILE(MAKE_DIRECTORY ${RPM_ROOTDIR}/SPECS)
      FILE(MAKE_DIRECTORY ${RPM_ROOTDIR}/SRPMS)

      #
      # We check whether if the provided spec file is
      # to be configure or not.
      #
      IF ("${ARGV1}" STREQUAL "")
        SET(SPECFILE_PATH "${RPM_ROOTDIR}/SPECS/${RPMNAME}.spec")
        SET(SPECFILE_NAME "${RPMNAME}.spec")
        MESSAGE(STATUS "Spec file ${RPM_ROOTDIR}/SPECS/${RPMNAME}.spec")
        FILE(WRITE ${RPM_ROOTDIR}/SPECS/${RPMNAME}.spec
             "# -*- rpm-spec -*-
Summary:        Intel Research, Berkeley ${RPMNAME}
Name:           ${RPMNAME}
Version:        ${PACKAGE_VERSION}
Release:        1
License:        GPL
Group:          Development
Source:         ${CPACK_SOURCE_PACKAGE_FILE_NAME}.tar.gz
BuildRoot:      %{_topdir}/%{name}-%{version}-%{release}-root
BuildRequires:	cmake

%define prefix /usr/local/${RPMNAME}
%define rpmprefix $RPM_BUILD_ROOT%{prefix}
%define srcdirname ${CPACK_SOURCE_PACKAGE_FILE_NAME}

%description
${RPMNAME} : No description for now

%define debug_package %{nil}

%prep
%setup -q -n %{srcdirname}

%build
cd ../%{srcdirname}/p2core/pel
python pel_gen.py
cd ../../..
rm -rf build_tree
mkdir build_tree
cd build_tree
cmake -DP2_LANG_DIR:STATIC=%{prefix}/lang -DCMAKE_INSTALL_PREFIX=%{rpmprefix} ../%{srcdirname}
make

%install
cd ../build_tree
make install

%clean
rm -rf %{srcdirname}
rm -rf build_tree

%files
%defattr(-,root,root,-)
%dir %{prefix}
%{prefix}/*

%changelog
")

      ELSE ("${ARGV1}" STREQUAL "")
        SET(SPECFILE_PATH "${ARGV1}")

        GET_FILENAME_COMPONENT(SPECFILE_EXT ${SPECFILE_PATH} EXT)
        IF ("${SPECFILE_EXT}" STREQUAL ".spec")
          # This is a 'ready-to-use' spec file which does not need to be CONFIGURED
          GET_FILENAME_COMPONENT(SPECFILE_NAME ${SPECFILE_PATH} NAME)
          MESSAGE(STATUS "Simple copy spec file <${SPECFILE_PATH}> --> <${RPM_ROOTDIR}/SPECS/${SPECFILE_NAME}>")
          CONFIGURE_FILE(
          ${SPECFILE_PATH}
          ${RPM_ROOTDIR}/SPECS/${SPECFILE_NAME}
          COPYONLY)
        ELSE ("${SPECFILE_EXT}" STREQUAL ".spec")
          # This is a to-be-configured spec file
          GET_FILENAME_COMPONENT(SPECFILE_NAME ${SPECFILE_PATH} NAME_WE)
          SET(SPECFILE_NAME "${SPECFILE_NAME}.spec")
          MESSAGE(STATUS "Configuring spec file <${SPECFILE_PATH}> --> <${RPM_ROOTDIR}/SPECS/${SPECFILE_NAME}>")
          CONFIGURE_FILE(
                 ${SPECFILE_PATH}
                 ${RPM_ROOTDIR}/SPECS/${SPECFILE_NAME}
                 @ONLY)
        ENDIF ("${SPECFILE_EXT}" STREQUAL ".spec")
      ENDIF("${ARGV1}" STREQUAL "")

      ADD_CUSTOM_TARGET(${RPMNAME}_srpm
          COMMAND cpack -G TGZ --config CPackSourceConfig.cmake
          COMMAND ${CMAKE_COMMAND} -E copy ${CPACK_SOURCE_PACKAGE_FILE_NAME}.tar.gz ${RPM_ROOTDIR}/SOURCES
          COMMAND ${CMAKE_COMMAND} -E remove ${CPACK_SOURCE_PACKAGE_FILE_NAME}.tar.gz
          COMMAND ${RPMBUILD_EXECUTABLE} -bs --define=\"_topdir ${RPM_ROOTDIR}\" --buildroot=${RPM_ROOTDIR}/tmp ${RPM_ROOTDIR}/SPECS/${SPECFILE_NAME}
       )

      ADD_CUSTOM_TARGET(${RPMNAME}_rpm
          COMMAND cpack -G TGZ --config CPackSourceConfig.cmake
          COMMAND ${CMAKE_COMMAND} -E copy ${CPACK_SOURCE_PACKAGE_FILE_NAME}.tar.gz ${RPM_ROOTDIR}/SOURCES
          COMMAND ${CMAKE_COMMAND} -E remove ${CPACK_SOURCE_PACKAGE_FILE_NAME}.tar.gz
          COMMAND ${RPMBUILD_EXECUTABLE} -bb --define=\"_topdir ${RPM_ROOTDIR}\" --buildroot=${RPM_ROOTDIR}/tmp ${RPM_ROOTDIR}/SPECS/${SPECFILE_NAME}
      )
    ENDMACRO(ADD_RPM_TARGETS)

  ENDIF (RPMBUILD_FOUND)

  endif(NOT RPMBUILD_FOUND)

ENDIF (UNIX)
