#!/bin/bash



$PREFIX/bin/python -m pip install . --no-deps --ignore-installed --no-cache-dir -vvv --global-option="--skip-install-fix" --install-option="--etc-root=$PREFIX"

python_loc=$($PREFIX/bin/python -c "from sysconfig import get_path; print(get_path('purelib'))")

python $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/bin/ELogin.{,c}sh
python $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/bin/ElementsEnv_group_{login,setup}.{,c}sh
python $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/bin/ElementsEnv_config.{,c}sh
python $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $python_loc/ElementsEnv/Login.py
python $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/etc/profile.d/elementsenv.sh
python $PREFIX/bin/FixInstallPath \$CONDA_PREFIX $PREFIX/etc/profile.d/elementsenv.csh

python $PREFIX/bin/FixInstallPath -n this_install_version "" $python_loc/ElementsEnv/Login.py

python $PREFIX/bin/FixInstallPath -n this_elementsenv_base \$CONDA_PREFIX/opt/euclid $python_loc/ElementsEnv/Login.py
python $PREFIX/bin/FixInstallPath -n this_elementsenv_base \$CONDA_PREFIX/opt/euclid $PREFIX/bin/ElementsEnv_config.{,c}sh

python $PREFIX/bin/FixInstallPath -n this_etc_install_prefix \$CONDA_PREFIX/etc $PREFIX/bin/ElementsEnv_config.{,c}sh
python $PREFIX/bin/FixInstallPath -n this_custom_prefix '""' $PREFIX/bin/ElementsEnv_config.{,c}sh

python $PREFIX/bin/FixInstallPath -n  this_install_prefix \$CONDA_PREFIX $PREFIX/bin/ElementsEnv_group_setup.{,c}sh
python $PREFIX/bin/FixInstallPath -n  this_install_prefix \$CONDA_PREFIX $PREFIX/bin/ElementsEnv_group_login.{,c}sh
python $PREFIX/bin/FixInstallPath -n  this_install_prefix \$CONDA_PREFIX $PREFIX/bin/ElementsEnv_config.{,c}sh

python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/eclipse_pythonpath_fix
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ELogin.csh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ELogin.sh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/E-Run
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ERun_autocompletion.sh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_config.csh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_config.sh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_login.csh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_login.sh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_setup.csh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/ElementsEnv_group_setup.sh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/runpy
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/StripPath.csh
python $PREFIX/bin/FixInstallPath -n this_python_version "" $PREFIX/bin/StripPath.sh



# Copy the [de]activate scripts to $PREFIX/etc/conda/[de]activate.d.
# This will allow them to be run on environment activation.
for CHANGE in "activate" "deactivate"
do
    mkdir -p "${PREFIX}/etc/conda/${CHANGE}.d"
    cp "${RECIPE_DIR}/${CHANGE}.sh" "${PREFIX}/etc/conda/${CHANGE}.d/${CHANGE}_elementsenv.sh"
done
