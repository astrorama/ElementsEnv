#!/usr/bin/env python
# $Id: ScriptTest.py 122763 2011-05-03 12:16:51Z hmdegaud $
""" Don't forget about the description """

from Euclid.Script import ConfigScript as Script

import logging
import os

__version__ = "$Id: ScriptTest.py 122763 2011-05-03 12:16:51Z hmdegaud $"


class ScriptTest(Script):
    _version = __version__
    _description = __doc__

    def defineOpts(self):
        parser = self.parser
        parser.set_defaults(toto_val="bla")
        parser.add_option(
            "-t", "--toto-val", help="set toto value [default %default]")

    def main(self):
        log = logging.getLogger()
        log.debug("This is a debug message")
        log.info("This is an info message")
        log.warning("This is a warning message")
        print(self.options.toto_val)
        return 0

if __name__ == '__main__':
    s = ScriptTest(usage="ScriptTest [options] path", use_config_file=True)
    s.run()
