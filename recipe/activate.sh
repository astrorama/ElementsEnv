#!/bin/bash

export BINARY_TAG=x86_64-conda_cos6-gcc93-o2g

export CMAKE_CONDA_PREFIX_PATH=${CONDA_PREFIX}:${CONDA_PREFIX}/share/ElementsEnv/cmake
export CMAKE_PROJECT_PATH=${HOME}/Work/Projects:${CONDA_PREFIX}/opt/euclid
export ELEMENTS_NAMING_DB_URL=https://pieclddj00.isdc.unige.ch/elementsnaming

export TEXINPUTS=${CONDA_PREFIX}/share/ElementsEnv/texmf
export CONDA_BUILD_SYSROOT=${CONDA_PREFIX}/x86_64-conda-linux-gnu/sysroot

export SOFTWARE_BASE_VAR=ELEMENTSENV_BASE
export ELEMENTSENV_BASE=${CONDA_PREFIX}/opt/euclid
export ELEMENTSENV_USE_BASE=yes

export CMAKEFLAGS="-DCPACK_REMOVE_SYSTEM_DEPS=ON \
 -DPYTHON_EXPLICIT_VERSION=3 \
 -DCMAKE_USE_CCACHE=YES \
 -DUSE_RPM_CMAKE_MACRO:BOOL=OFF \
 -DRPMBUILD_EXTRA_ARGS=\"--dbpath=${CONDA_PREFIX}/var/lib/rpm --define '__cmake ${CONDA_PREFIX}/bin/cmake' \" \
 -DUSE_ENV_FLAGS:BOOL=OFF \
 -DCMAKE_SUPPRESS_REGENERATION=ON "


export LANG='en_US.UTF-8'
unset CFLAGS
unset CXXFLAGS
unset CPPFLAGS
unset DEBUG_CFLAGS
unset DEBUG_CXXFLAGS
unset DEBUG_CPPFLAGS
unset LDFLAGS

if [ -z "$E_BANNER" ]; then
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_login.sh &> /dev/null
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_setup.sh &> /dev/null
else
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_login.sh
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_setup.sh
fi

. ${CONDA_PREFIX}/bin/ERun_autocompletion.sh


