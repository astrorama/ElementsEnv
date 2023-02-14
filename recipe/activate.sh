#!/bin/bash

export LANG='en_US.UTF-8'
export SOFTWARE_BASE_VAR=ELEMENTSENV_BASE
export ELEMENTSENV_BASE=${CONDA_PREFIX}/opt/euclid
export ELEMENTSENV_USE_BASE=yes
export ELEMENTSENVPROJECTPATH=${ELEMENTSENV_BASE}
export CMAKE_CONDA_PREFIX_PATH=${CONDA_PREFIX}:${CONDA_PREFIX}/share/ElementsEnv/cmake
export CMAKE_PROJECT_PATH=${HOME}/Work/Projects:${CONDA_PREFIX}/opt/euclid
export CMAKE_PREFIX_PATH=${CONDA_PREFIX}/share/ElementsEnv/cmake:${CONDA_PREFIX}:${CONDA_PREFIX}/x86_64-conda-linux-gnu/sysroot/usr
export ELEMENTS_NAMING_DB_URL=https://pieclddj00.isdc.unige.ch/elementsnaming

export TEXINPUTS=${CONDA_PREFIX}/share/ElementsEnv/texmf
export CONDA_BUILD_SYSROOT=${CONDA_PREFIX}/x86_64-conda-linux-gnu/sysroot


if [ -z "$E_BANNER" ]; then
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_login.sh &> /dev/null
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_setup.sh &> /dev/null
else
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_login.sh
	. ${CONDA_PREFIX}/bin/ElementsEnv_group_setup.sh
fi

. ${CONDA_PREFIX}/bin/ERun_autocompletion.sh




# https://euclid.roe.ac.uk/issues/17998
export QT_PLUGIN_PATH=$CONDA_PREFIX/plugins
export FONTCONFIG_FILE=$CONDA_PREFIX/etc/fonts/fonts.conf
export FONTCONFIG_PATH=$CONDA_PREFIX/etc/fonts/

