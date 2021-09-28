#!/bin/bash

pushd ${PREFIX}/lib/python3.9
	if [ ! -f _sysconfigdata_x86_64_conda_linux_gnu.py ]; then
		ln -s _sysconfigdata__linux_x86_64-linux-gnu.py _sysconfigdata_x86_64_conda_linux_gnu.py &> $PREFIX/.messages.txt
	fi
popd

