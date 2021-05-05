"""
This is the initial setup for the Euclid namespace package
"""
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)  # @ReservedAssignment

__author__  = 'Hubert Degaudenzi'

import sys

# hooks and other customizations are not used ith iPython
_is_ipython = hasattr(__builtins__, '__IPYTHON__') or 'IPython' in sys.modules
_cleanup_list = []

# Add some infrastructure if we are being imported via a Jupyter Kernel ------
if _is_ipython:
    from IPython import get_ipython
    _ip = get_ipython()
    _cleanup_list.append(_ip)
    if hasattr(_ip,"kernel"):
        from .Login import LoginScript
        from .Env import Environment
        # _option_list = ["--debug"]
        _usage = "ELogin [options] [type]"
        _option_list = []
        _login_script = LoginScript(usage=_usage)
        _login_script.parseOpts(_option_list)
        _ev = _login_script.setEnv()
        _al = _login_script.setAliases()
        _ex = _login_script.setExtra()

        from IPython.core import magic_arguments, magic
 
        @magic.magics_class
        class Magics(magic.Magics):

            @magic.line_magic
            def elogin(self, line):
                global _login_script
                global _ev, _al, _ex
                if line:
                    option_list = line.split()
                    _login_script = LoginScript(usage=_usage)
                    _login_script.parseOpts(option_list)
                    _ev = _login_script.setEnv()
                    _al = _login_script.setAliases()
                    _ex = _login_script.setExtra()

            @magic.line_magic
            def erun(self, line):
                import site, os, sys
                from .Run.Script import ERun
                global _ev
                if line:
                    option_list = line.split()
                    er = ERun(option_list)
                    er._makeEnv()
                    if not er.cmd:
                        _ev = Environment()
                        for key, value in er._getEnv().items():
                            _ev[key] = value
                        sys.path = _ev["PYTHONPATH"].split(os.pathsep) + sys.path
                    else:
                        er.runCmd()

        _ip.register_magics(Magics)

# _cleanup 
import atexit
def _cleanup():

    import sys
    # destroy Euclid module
    del sys.modules[ 'Euclid' ]

atexit.register( _cleanup )
del _cleanup, atexit, sys
