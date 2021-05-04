from __future__ import absolute_import

import logging

def _createLogger():
    l = logging.getLogger('EuclidWrapper')
    l.setLevel(logging.INFO)
    _console = logging.StreamHandler()
    _formatter = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)5s : %(message)s', datefmt='%Y-%m-%dT%X%Z')
    _console.setFormatter(_formatter)
    l.addHandler(_console)
    return l

logger = _createLogger()