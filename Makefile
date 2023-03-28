SGS_SEARCH := /opt/SGS /cvmfs/euclid-dev.in2p3.fr/SGS /cvmfs/euclid.in2p3.fr/SGS

ifndef SGS_MAKEFILE
_makefile := share/sgsenv/make/SGSTargets.makefile
SGS_MAKE_LIB_LIST := $(foreach dir,$(SGS_SEARCH),$(wildcard $(dir)/$(_makefile)))
SGS_MAKEFILE := $(firstword $(SGS_MAKE_LIB_LIST))
endif

ifndef SGS_MAKEFILE
$(error SGS_MAKEFILE not found in $(SGS_MAKE_LIB_LIST):$(SGS_SEARCH))
endif
SGS := $(dir $(SGS_MAKEFILE))/../../../

include $(SGS_MAKEFILE)




FORCE:
