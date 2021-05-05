from . import path, Error
from .Version import getVersionDirs, versionSort
from ..Platform import getSearchList


import os
import logging


log = logging.getLogger(__name__)


class NotFoundError(Error):

    '''
    Generic error for configuration elements that are not found.
    '''


class MissingManifestError(NotFoundError):

    '''
    The manifest.xml for a project was not found.
    '''


class MissingProjectError(NotFoundError):

    '''
    The manifest.xml for a project was not found.
    '''

    def __init__(self, *args):
        super(MissingProjectError, self).__init__(*args)
        self.name, self.version, self.platform, self.path = args

    def __str__(self):
        return 'cannot find project {0} {1} for {2} in {3}'.format(*self.args)


def findProject(name, version, platform):
    '''
    Find a Elements-based project in the directories specified in the 'path'
    variable.
    @param name: name of the project (case sensitive for local projects)
    @param version: version of the project
    @param platform: binary platform id

    @return path to the project binary directory
    '''
    log.debug('findProject(%r, %r, %r)', name, version, platform)
    project_dir = None
    # standard project suffixes
    suffixes = [os.path.join(name, version),
                '{0}_{1}'.format(name, version),
                os.path.join(name.upper(), '{0}_{1}'.format(name.upper(), version))]
    bindir = os.path.join('InstallArea', platform)
    # special case: with the default 'latest' version we allow the plain name
    if version != 'latest':
        # an explicit version is requested. It will be found either with the matching version
        # subdirectory or with the correspond manifest.xml. The search is done
        # in each path.
        for b in path:
            for d in [os.path.join(b, s, bindir)
                      for s in suffixes]:
                log.debug('check %s', d)
                if os.path.exists(d):
                    log.debug('OK')
                    project_dir = d
                    break

            if not project_dir:
                # look for implicit version. The manifest.xml file has to be
                # checked.
                d = os.path.join(b, name, bindir)
                log.debug('check %s', d)
                if os.path.exists(d):
                    # manifest.xml to be checked for the version
                    manifest = os.path.join(d, "manifest.xml")
                    if os.path.exists(manifest):
                        (_, p_version) = getProjectFromManifest(manifest)
                        if p_version == version:
                            project_dir = d
                            break
            else:
                break

    else:
        # The version is latest. The last project with the highest version subdir or
        # The first project without a version subdir met
        # in the path will be used.
        for b in path:
            if os.path.exists(os.path.join(b, name)):
                all_versions = versionSort(
                    getVersionDirs(os.path.join(b, name), bindir))
                if all_versions:
                    project_dir = os.path.join(
                        b, name, all_versions[-1], bindir)
                    break

                if not project_dir:
                    d = os.path.join(b, name, bindir)
                    log.debug('check %s', d)
                    if os.path.exists(d):
                        project_dir = d
                        break

    if not project_dir:
        raise MissingProjectError(name, version, platform, path)

    return project_dir


def parseManifest(manifest):
    '''
    Extract the list of required projects from a manifest.xml
    file.

    @param manifest: path to the manifest file
    @return: tuple with ([projects...],) as (name, version) pairs
    '''
    from xml.dom.minidom import parse
    m = parse(manifest)

    def _iter(parent, child):
        '''
        Iterate over the tags in <parent><child/><child/></parent>.
        '''
        for pl in m.getElementsByTagName(parent):
            for c in pl.getElementsByTagName(child):
                yield c
    # extract the list of used (project, version) from the manifest
    used_projects = [(p.attributes['name'].value, p.attributes['version'].value)
                     for p in _iter('used_projects', 'project')]
    # extract the list of data packages
#    data_packages = [(p.attributes['name'].value, p.attributes['version'].value)
#                     for p in _iter('used_data_pkgs', 'package')]
    data_packages = []
    return (used_projects, data_packages)


def getProjectFromManifest(manifest):
    """
    Extract the project name and version from a manifest.xml
    file.

    @param manifest: path to the manifest file
    @return: tuple with the project name and version as (name, version) 
    """
    from xml.dom.minidom import parse
    m = parse(manifest)

    def _iter(parent, child):
        '''
        Iterate over the tags in <parent><child/><child/></parent>.
        '''
        for pl in m.getElementsByTagName(parent):
            for c in pl.getElementsByTagName(child):
                yield c
    # extract the list of used (project, version) from the manifest
    projects = [(p.attributes['name'].value, p.attributes['version'].value)
                for p in _iter('manifest', 'project')]

    return projects[0]


def getEnvXmlPath(project, version, platform):
    '''
    Return the list of directories to be added to the Env XML search path for
    a given project.
    '''
    pdir = findProject(project, version, platform)
    search_path = [pdir]
    # manifests to parse
    manifests = [os.path.join(pdir, 'manifest.xml')]
    while manifests:
        manifest = manifests.pop(0)
        if not os.path.exists(manifest):
            raise MissingManifestError(manifest)
        projects, _ = parseManifest(manifest)
        # add the project directories ...
        # search in all binary tag. Starting with the default one
        pdirs = []
        for p, v in projects:
            p_dirs = None
            for b in getSearchList(platform):
                try:
                    p_dirs = findProject(p, v, b)
                except MissingProjectError:
                    pass
                if p_dirs:
                    break
            if not p_dirs:
                raise MissingProjectError(p, v, platform, path)
            pdirs.append(p_dirs)

        search_path.extend(pdirs)


        # ... and their manifests to the list of manifests to parse
        manifests.extend([os.path.join(pdir, 'manifest.xml')
                          for pdir in pdirs])

    def _unique(iterable):
        returned = set()
        for i in iterable:
            if i not in returned:
                returned.add(i)
                yield i
    return list(_unique(search_path))
