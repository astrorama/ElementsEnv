#!/bin/bash

$PYTHON -m pip install . --no-deps --ignore-installed --no-cache-dir -vvv --global-option="--skip-install-fix" --install-option="--etc-root=$PREFIX"

python_loc=$($PYTHON -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

$PYTHON $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/bin/ELogin.{,c}sh
$PYTHON $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/bin/ElementsEnv_group_{login,setup}.{,c}sh
$PYTHON $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/bin/ElementsEnv_config.{,c}sh
$PYTHON $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $python_loc/ElementsEnv/Login.py
$PYTHON $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/etc/profile.d/elementsenv.sh
$PYTHON $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/etc/profile.d/elementsenv.csh

$PYTHON $PREFIX/bin/FixInstallPath -n this_install_version "" $python_loc/ElementsEnv/Login.py

$PYTHON $PREFIX/bin/FixInstallPath -n this_euclid_base \$CONDA_PREFIX/opt/euclid $python_loc/ElementsEnv/Login.py
$PYTHON $PREFIX/bin/FixInstallPath -n this_euclid_base \$CONDA_PREFIX/opt/euclid $PREFIX/bin/ElementsEnv_config.{,c}sh
$PYTHON $PREFIX/bin/FixInstallPath -n this_etc_install_prefix \$CONDA_PREFIX/etc $PREFIX/bin/ElementsEnv_config.{,c}sh

$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/eclipse_pythonpath_fix
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ELogin.csh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ELogin.sh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/E-Run
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ERun_autocompletion.sh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_config.csh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_config.sh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_login.csh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_login.sh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_setup.csh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_setup.sh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/runpy
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/StripPath.csh
$PYTHON $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/StripPath.sh



# Copy the [de]activate scripts to $PREFIX/etc/conda/[de]activate.d.
# This will allow them to be run on environment activation.
for CHANGE in "activate" "deactivate"
do
    mkdir -p "${PREFIX}/etc/conda/${CHANGE}.d"
    cp "${RECIPE_DIR}/${CHANGE}.sh" "${PREFIX}/etc/conda/${CHANGE}.d/zzz-elementsenv_${CHANGE}.sh"
done

