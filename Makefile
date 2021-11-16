NAME := elementsenv
VERSION :=  3.18.0

SGS_MAKE_LIB := SGSTargets.makefile
SGS_SEARCH :=  ~/Work/Projects/SGS /opt/euclid-dev.in2p3.fr/CentOS7/SGS /cvmfs/euclid-dev.in2p3.fr/CentOS7/SGS 

ifndef SGS_MAKEFILE
_makefile := lib/python3.9/site-packages/sgsenv/SGSTargets.makefile
SGS_MAKE_LIB_LIST := $(foreach dir,$(SGS_SEARCH),$(wildcard $(dir)/$(_makefile)))
SGS_MAKEFILE := $(firstword $(SGS_MAKE_LIB_LIST))
endif

SGS := $(dir $(SGS_MAKEFILE))/../../../../

include $(SGS_MAKEFILE)

.PHONY: FORCE


configure:
	$(MAKE) -f $(SGS_MAKEFILE) configure
	$(call setup_env)
	$(MAKE) configure-conda



package: FORCE
	$(MAKE) conda-package




