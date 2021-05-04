'''
Created on Jul 2, 2011

@author: mplajner
'''

from xml.dom import minidom
import logging
from pickle import load, dump
from hashlib import md5
import os


class XMLFile(object):

    '''Takes care of XML file operations such as reading and writing.'''

    def __init__(self):
        self.xml_result = '<?xml version="1.0" encoding="UTF-8"?>'
        self.xml_result += '<env:config xmlns:env="EnvSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="EnvSchema ./EnvSchema.xsd ">'
        self.xml_result += os.linesep
        self.declaredVars = []
        self.log = logging.getLogger('XMLFile')

    @staticmethod
    def variable(path, namespace='EnvSchema', name=None):
        '''Returns list containing name of variable, action and value.

        @param path: a file name or a file-like object

        If no name given, returns list of lists of all variables and locals(instead of action 'local' is filled).
        '''
        is_filename = type(path) is str
        if is_filename:
            checksum = md5()
            checksum.update(open(path, 'rb').read())
            checksum = checksum.digest()

            # preparsed file
            cpath = path + "c"
            try:
                f = open(cpath, 'rb')
                oldsum, data = load(f)
                if oldsum == checksum:
                    return data
            except IOError:
                pass
            except EOFError:
                pass

            caller = path
        else:
            caller = None

        # Get file
        doc = minidom.parse(path)
        if namespace == '':
            namespace = None

        ELEMENT_NODE = minidom.Node.ELEMENT_NODE
        # Get all variables
        nodes = doc.getElementsByTagNameNS(namespace, "config")[0].childNodes
        variables = []
        for node in nodes:
            # if it is an element node
            if node.nodeType == ELEMENT_NODE:
                action = str(node.localName)

                if action == 'include':
                    if node.childNodes:
                        value = str(node.childNodes[0].data)
                    else:
                        value = ''
                    variables.append(
                        (action, (value, caller, str(node.getAttribute('hints')))))

                elif action == 'search_path':
                    if node.childNodes:
                        value = str(node.childNodes[0].data)
                    else:
                        value = ''
                    variables.append((action, (value, None, None)))

                else:
                    varname = str(node.getAttribute('variable'))
                    if name and varname != name:
                        continue

                    if action == 'declare':
                        variables.append(
                            (action, (varname, str(node.getAttribute('type')), str(node.getAttribute('local')))))
                    else:
                        if node.childNodes:
                            value = str(node.childNodes[0].data)
                        else:
                            value = ''
                        variables.append((action, (varname, value, None)))

        if is_filename:
            try:
                f = open(cpath, 'wb')
                dump((checksum, variables), f, protocol=2)
                f.close()
            except IOError:
                pass
        return variables

    def resetWriter(self):
        '''resets the buffer of writer'''
        self.xml_result = '<?xml version="1.0" encoding="UTF-8"?>'
        self.xml_result += '<env:config xmlns:env="EnvSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="EnvSchema ./EnvSchema.xsd ">'
        self.xml_result += os.linesep
        self.declaredVars = []

    def writeToFile(self, output_file=None):
        '''Finishes the XML input and writes XML to file.'''
        if output_file is None:
            raise IOError("No output file given")
        self.xml_result += '</env:config>'

        doc = minidom.parseString(self.xml_result)
        with open(output_file, "w") as f:
            f.write(doc.toxml())

        return output_file

    def writeVar(self, varName, action, value, vartype='list', local=False):
        '''Writes a action to a file. Declare undeclared elements (non-local list is default type).'''
        if action == 'declare':
            self.xml_result += '<env:declare variable="' + varName + '" type="' + \
                vartype.lower() + '" local="' + (str(local)).lower() + \
                '" />' + os.linesep
            self.declaredVars.append(varName)
            return

        if varName not in self.declaredVars:
            self.xml_result += '<env:declare variable="' + varName + '" type="' + \
                vartype + '" local="' + \
                (str(local)).lower() + '" />' + os.linesep
            self.declaredVars.append(varName)
        self.xml_result += '<env:' + action + ' variable="' + \
            varName + '">' + value + '</env:' + action + '>' + os.linesep
