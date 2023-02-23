cmake_minimum_required(VERSION 3.22)

project(ST_ElementsEnv NONE)
find_package(Conda)

set(st_elementsenv_OVERRIDE_VERSION TRUE)

sgs_conda_project(
	LIBRARY st_elementsenv linux-64 .
)



