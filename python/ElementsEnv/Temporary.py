""" create temporary structure for remote buids """

from shutil import rmtree

import os

from tempfile import mkdtemp, mkstemp


class TempDir(object):

    """Class to create a temporary directory."""

    def __init__(self, suffix="", prefix="tmp", base_dir=None, keep_var="KEEPTEMPDIR"):
        """Constructor.

        'keep_var' is used to define which environment variable will prevent the
        deletion of the directory.

        The other arguments are the same as tempfile.mkdtemp.
        """
        self._keep_var = keep_var
        self._name = mkdtemp(suffix, prefix, base_dir)

    def getName(self, stem=None):
        """Returns the name of the temporary directory"""

        name = self._name

        if stem:
            name = os.path.join(name, stem)

        return name

    def __str__(self):
        """Convert to string."""
        return self.getName()

    def __del__(self):
        """Destructor.

        Remove the temporary directory.
        """
        if self._name:
            if self._keep_var in os.environ:
                import logging
                logging.info("%s set: I do not remove the temporary directory '%s'",
                             self._keep_var, self._name)
                return
            rmtree(self._name)


class TempFile:

    """ class to create a temporary file """

    def __init__(self):
        """ Constructor """
        self._file = None
        self.name = ''

        fd, name = mkstemp()
        self.name = name
        self._file = os.fdopen(fd, "w+")

    def __del__(self):
        """ Destructor """
        if self._file:
            self._file.close()
            os.remove(self.name)

    def __getattr__(self, attr):
        return getattr(self._file, attr)
