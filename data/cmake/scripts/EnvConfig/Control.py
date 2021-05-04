'''
Created on Jun 27, 2011

@author: mplajner
'''
from . import xmlModule

import os
from time import gmtime, strftime

from . import Variable
import EnvConfig  # @UnresolvedImport
import logging


class Environment(object):

    '''object to hold settings of environment'''

    def __init__(self, load_from_system=True, use_as_writer=False, search_path=None):
        '''Initial variables to be pushed and setup

        append switch between append and prepend for initial variables.
        load_from_system causes variable`s system value to be loaded on first encounter.
        If use_as_writer == True than every change to variables is recorded to XML file.
        reportLevel sets the level of messaging.
        '''
        self.log = logging.getLogger('Environment')

        self.separator = ':'

        # Prepare the internal search path for xml files (used by 'include'
        # elements)
        if search_path is None:
            self.searchPath = []
        else:
            self.searchPath = list(search_path)

        self.actions = {}
        self.actions['include'] = lambda n, c, h: self.loadXML(
            self._locate(n, c, h))
        self.actions['append'] = lambda n, v, _: self.append(n, v)
        self.actions['prepend'] = lambda n, v, _: self.prepend(n, v)
        self.actions['set'] = lambda n, v, _: self.set(n, v)
        self.actions['unset'] = lambda n, v, _: self.unset(n, v)
        self.actions['default'] = lambda n, v, _: self.default(n, v)
        self.actions['remove'] = lambda n, v, _: self.remove(n, v)
        self.actions[
            'remove-regexp'] = lambda n, v, _: self.remove_regexp(n, v)
        self.actions['declare'] = self.declare
        self.actions['search_path'] = lambda n, _1, _2: self.searchPath.extend(
            n.split(self.separator))

        self.variables = {}

        self.loadFromSystem = load_from_system
        self.asWriter = use_as_writer
        if use_as_writer:
            self.writer = xmlModule.XMLFile()
            self.startXMLinput()

        self.loadedFiles = set()

        # Prepare the stack for the directory of the loaded file(s)
        self._fileDirStack = []
        # Note: cannot use self.declare() because we do not want to write out
        #       the changes to ${.}
        dot = Variable.Scalar('.', local=True)
        dot.expandVars = False
        dot.set('')
        self.variables['.'] = dot

    def _locate(self, filename, caller=None, hints=None):
        '''
        Find 'filename' in the internal search path.
        '''
        from os.path import isabs, isfile, join, dirname, normpath, abspath
        if isabs(filename):
            return filename

        self.log.debug('looking for %s', filename)
        if hints is None:
            hints = []
        elif type(hints) is str:
            hints = hints.split(self.separator)

        if caller:
            calldir = dirname(caller)
            localfile = join(calldir, filename)
            self.log.debug('trying %s', localfile)
            if isfile(localfile):
                self.log.debug('OK (local file)')
                return localfile
            # allow for relative hints
            hints = [join(calldir, hint) for hint in hints]

        sp = EnvConfig.path + self.searchPath + hints

        def candidates():
            """ find file candidates """
            for d in sp:
                f = normpath(join(d, filename))
                self.log.debug('trying %s', f)
                yield f
        try:
            f = next((abspath(f) for f in candidates() if isfile(f)))
            self.log.debug('OK')
            return f
        except StopIteration:
            from errno import ENOENT
            raise OSError(ENOENT, 'cannot find file in %r' % sp, filename)

    def vars(self, strings=True):
        '''returns dictionary of all variables optionally converted to string'''
        if strings:
            return dict([(n, v.value(True)) for n, v in self.variables.items()])
        else:
            return self.variables

    def var(self, name):
        '''Gets a single variable. If not available then tries to load from system.'''
        if name in self.variables:
            return self.variables[name]
        else:
            return os.environ[name]

    def search(self, var_name, expr, reg_exp=False):
        '''Searches in a variable for a value.'''
        return self.variables[var_name].search(expr, reg_exp)

    def _guessType(self, varname):
        '''
        Guess the type of the variable from its name: if the name contains
        'PATH' or 'DIRS', then the variable is a list, otherwise it is a scalar.
        '''
        # make the comparison case insensitive
        varname = varname.upper()
        if 'PATH' in varname or 'DIRS' in varname:
            return 'list'
        else:
            return 'scalar'

    def declare(self, name, vartype, local):
        '''Creates an instance of new variable. It loads values from the OS if the variable is not local.'''
        if self.asWriter:
            self._writeVarToXML(name, 'declare', '', vartype, local)

        if not isinstance(local, bool):
            if str(local).lower() == 'true':
                local = True
            else:
                local = False

        if name in self.variables.keys():
            if self.variables[name].local != local:
                raise Variable.EnvError(name, 'redeclaration')
            else:
                if vartype.lower() == "list":
                    if not isinstance(self.variables[name], Variable.List):
                        raise Variable.EnvError(name, 'redeclaration')
                else:
                    if not isinstance(self.variables[name], Variable.Scalar):
                        raise Variable.EnvError(name, 'redeclaration')

        if vartype.lower() == "list":
            a = Variable.List(name, local)
        else:
            a = Variable.Scalar(name, local)

        if self.loadFromSystem and not local and name in os.environ:
            # disable var expansion when importing from the environment
            a.expandVars = False
            a.set(os.environ[name], os.pathsep, environment=self.variables)
            a.expandVars = True

        self.variables[name] = a

    def append(self, name, value):
        '''Appends to an existing variable.'''
        if self.asWriter:
            self._writeVarToXML(name, 'append', value)
        else:
            if name not in self.variables:
                self.declare(name, self._guessType(name), False)
            self.variables[name].append(value, self.separator, self.variables)

    def prepend(self, name, value):
        '''Prepends to an existing variable, or create a new one.'''
        if self.asWriter:
            self._writeVarToXML(name, 'prepend', value)
        else:
            if name not in self.variables:
                self.declare(name, self._guessType(name), False)
            self.variables[name].prepend(value, self.separator, self.variables)

    def set(self, name, value):
        '''Sets a single variable - overrides any previous value!'''
        name = str(name)
        if self.asWriter:
            self._writeVarToXML(name, 'set', value)
        else:
            if name not in self.variables:
                self.declare(name, self._guessType(name), False)
            self.variables[name].set(value, self.separator, self.variables)

    def default(self, name, value):
        '''Sets a single variable only if it is not already set!'''
        name = str(name)
        if self.asWriter:
            self._writeVarToXML(name, 'default', value)
        else:
            # Here it is different from the other actions because after a 'declare'
            # we cannot tell if the variable was already set or not.
            # FIXME: improve declare() to allow for a default.
            if name not in self.variables:
                if self._guessType(name) == 'list':
                    v = Variable.List(name, False)
                else:
                    v = Variable.Scalar(name, False)
                if self.loadFromSystem and name in os.environ:
                    v.set(
                        os.environ[name], os.pathsep, environment=self.variables)
                else:
                    v.set(value, self.separator, environment=self.variables)
                self.variables[name] = v
            else:
                v = self.variables[name]
                if not v.val:
                    v.set(value, self.separator, environment=self.variables)

    def unset(self, name, value=None):
        '''Unsets a single variable to an empty value - overrides any previous value!'''
        if self.asWriter:
            self._writeVarToXML(name, 'unset', '')
        else:
            if name in self.variables:
                del self.variables[name]

    def remove(self, name, value, regexp=False):
        '''Remove value from variable.'''
        if self.asWriter:
            self._writeVarToXML(name, 'remove', value)
        else:
            if name not in self.variables:
                self.declare(name, self._guessType(name), False)
            self.variables[name].remove(value, self.separator, regexp)

    def remove_regexp(self, name, value):
        self.remove(name, value, True)

    def searchFile(self, filename, var_name):
        '''Searches for appearance of variable in a file.'''
        xmlfile = xmlModule.XMLFile()
        variable = xmlfile.variable(filename, name=var_name)
        return variable

    def loadXML(self, file_name=None, namespace='EnvSchema'):
        '''Loads XML file for input variables.'''
        xmlfile = xmlModule.XMLFile()
        file_name = self._locate(file_name)
        if file_name in self.loadedFiles:
            # ignore recursion
            return
        self.loadedFiles.add(file_name)
        dot = self.variables['.']
        # push the previous value of ${.} onto the stack...
        self._fileDirStack.append(dot.value())
        # ... and update the variable
        dot.set(os.path.dirname(file_name))
        variables = xmlfile.variable(file_name, namespace=namespace)
        for i, (action, args) in enumerate(variables):
            if action not in self.actions:
                self.log.error('Node {0}: No action taken with var "{1}". '
                               'Probably wrong action argument: "{2}".'.format(i, args[0], action))
            else:
                self.actions[action](*args)
        # restore the old value of ${.}
        dot.set(self._fileDirStack.pop())
        # ensure that a change of ${.} in the file is reverted when exiting it
        self.variables['.'] = dot

    def startXMLinput(self):
        '''Renew writer for new input.'''
        self.writer.resetWriter()

    def finishXMLinput(self, output_file=''):
        '''Finishes input of XML file and closes the file.'''
        self.writer.writeToFile(output_file)

    def writeToFile(self, file_name, shell='sh'):
        '''Creates an output file with a specified name to be used for setting variables by sourcing this file'''
        f = open(file_name, 'w')
        if shell == 'sh':
            f.write('#!/bin/bash' + os.linesep)
            for variable in self.variables:
                if not self[variable].local:
                    f.write(
                        'export ' + variable + '=' + self[variable].value(True, os.pathsep) + os.linesep)
        elif shell == 'csh':
            f.write('#!/bin/csh' + os.linesep)
            for variable in self.variables:
                if not self[variable].local:
                    f.write(
                        'setenv ' + variable + ' ' + self[variable].value(True, os.pathsep) + os.linesep)
        else:
            f.write('')
            f.write('REM This is an enviroment settings file generated on ' +
                    strftime("%a, %d %b %Y %H:%M:%S", gmtime()) + os.linesep)
            for variable in self.variables:
                if not self[variable].local:
                    f.write(
                        'set ' + variable + '=' + self[variable].value(True, os.pathsep) + os.linesep)

        f.close()

    def writeToXMLFile(self, file_name):
        '''Writes the current state of environment to a XML file.

        NOTE: There is no trace of actions taken, variables are written with a set action only.
        '''
        writer = xmlModule.XMLFile()
        for var_name in self.variables:
            if var_name == '.':
                # this is an internal transient variable
                continue
            writer.writeVar(
                var_name, 'set', self.variables[var_name].value(True, self.separator))
        writer.writeToFile(file_name)

    def presetFromSystem(self):
        '''Loads all variables from the current system settings.'''
        for k, v in os.environ.items():
            if k not in self.variables:
                self.set(k, v)

    def process(self):
        '''
        Call the variable processors on all the variables.
        '''
        for v in self.variables.values():
            v.val = v.process(v.val, self.variables)

    def _concatenate(self, value):
        '''Returns a variable string with separator separator from the values list'''
        stri = ""
        for it in value:
            stri += it + self.separator
        stri = stri[0:len(stri) - 1]
        return stri

    def _writeVarToXML(self, name, action, value, vartype='list', local='false'):
        '''Writes single variable to XML file.'''
        if isinstance(value, list):
            value = self._concatenate(value)
        self.writer.writeVar(name, action, value, vartype, local)

    def __getitem__(self, key):
        return self.variables[key]

    def __setitem__(self, key, value):
        if key in self.variables.keys():
            self.log.warning(
                'Addition canceled because of duplicate entry. Var: "%s" value: "%s".', key, value)
        else:
            self.append(key, value)

    def __delitem__(self, key):
        del self.variables[key]

    def __iter__(self):
        for i in self.variables:
            yield i

    def __contains__(self, item):
        return item in self.variables.keys()

    def __len__(self):
        return len(self.variables.keys())
