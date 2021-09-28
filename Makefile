CONDA ?= /cvmfs/euclid-dev.in2p3.fr/CentOS7/EDEN-2.1

.PHONY: FORCE

package: FORCE
	mkdir -p dist
	source ${CONDA}/bin/activate && conda build recipe -c conda-forge --output-folder ./dist

install:
	source ${CONDA}/bin/activate && PYTHON=python PREFIX=${CONDA} RECIPE_DIR=./recipe ./recipe/build.sh 
	source ${CONDA}/bin/activate && PYTHON=python PREFIX=${CONDA} RECIPE_DIR=./recipe ./recipe/post-link.sh



