

import os
import logging

import Euclid.Run

from string import Template


def main():
    '''
    Script to generate a local development project.
    '''
    from optparse import OptionParser
    from Euclid.Run.Options import addSearchPath, addOutputLevel, addPlatform
    from Euclid.Run.Lookup import findProject, MissingProjectError

    parser = OptionParser(usage='%prog [options] Project version')

    addSearchPath(parser)
    addOutputLevel(parser)
    addPlatform(parser)

    parser.add_option('--name', action='store',
                      help='Name of the local project [default: "<proj>Dev_<vers>"].')

    # Note: the profile is not used in the script class, but in the wrapper
    #       it is added to the parser to appear in the help and for checking
    parser.add_option('--profile', action='store_true',
                      help='Print some profile informations about the execution.')

    opts, args = parser.parse_args()

    logging.basicConfig(level=opts.log_level)

    try:
        project, version = args
    except ValueError:
        parser.error('wrong number of arguments')

    if not opts.name:
        opts.name = '{project}Dev_{version}'.format(
            project=project, version=version)
        local_project, local_version = project + 'Dev', version
    else:
        local_project, local_version = opts.name, 'HEAD'

    devProjectDir = os.path.join(opts.user_area, opts.name)

    # Check options
    if not opts.user_area:
        parser.error(
            'user area not defined (environment variable User_release_area or option --user-area)')

    if os.path.exists(devProjectDir):
        parser.error('directory "%s" already exist' % devProjectDir)

    # ensure that the project we want to use can be found

    # prepend dev dirs to the search path
    if opts.dev_dirs:
        Euclid.Run.path[:] = map(str, opts.dev_dirs) + Euclid.Run.path

    try:
        projectDir = findProject(project, version, opts.platform)
        logging.info('using %s %s from %s', project, version, projectDir)
    except MissingProjectError as x:
        parser.error(str(x))

    use_cmake = os.path.exists(os.path.join(projectDir, 'manifest.xml'))
    if not use_cmake:
        logging.warning(
            '%s %s does not seem a CMake project', project, version)

    # Create the dev project
    if not os.path.exists(opts.user_area):
        logging.debug(
            'creating user release area directory "%s"', opts.user_area)
        os.makedirs(opts.user_area)

    logging.debug('creating directory "%s"', devProjectDir)
    os.makedirs(devProjectDir)

    data = dict(project=project,
                version=version,
                search_path=' '.join(['"%s"' % p for p in Euclid.Run.path]),
                search_path_repr=repr(Euclid.Run.path),
                search_path_env=os.pathsep.join(Euclid.Run.path),
                use_cmake=(use_cmake and 'yes' or ''),
                PROJECT=project.upper(),
                local_project=local_project,
                local_version=local_version,
                cmt_project=opts.name)

    # FIXME: improve generation of searchPath files, so that they match the
    # command line
    templateDir = os.path.join(os.path.dirname(__file__), 'templates')
    templates = ['CMakeLists.txt', 'toolchain.cmake', 'Makefile',
                 'searchPath.py', 'searchPath.cmake',
                 'build_env.sh', 'build_env.csh']
    if opts.nightly:
        data['slot'], data['day'] = opts.nightly
        templates.append('nightly.cmake')
    else:
        data['slot'] = data['day'] = ''

    # for backward compatibility, we create the CMT configuration
    if not use_cmake:
        templates.append('cmt/project.cmt')
        os.makedirs(os.path.join(devProjectDir, 'cmt'))

    for templateName in templates:
        t = Template(open(os.path.join(templateDir, templateName)).read())
        logging.debug('creating "%s"', templateName)
        open(os.path.join(devProjectDir, templateName), 'w').write(
            t.substitute(data))

    # When the project name is not the same as the local project name, we need a
    # fake *Sys package for SetupProject (CMT only).
    if not use_cmake and project != local_project:
        t = Template(
            open(os.path.join(templateDir, 'cmt/requirements_')).read())
        templateName = os.path.join(local_project + 'Sys', 'cmt/requirements')
        os.makedirs(os.path.dirname(os.path.join(devProjectDir, templateName)))
        logging.debug('creating "%s"', templateName)
        open(os.path.join(devProjectDir, templateName), 'w').write(
            t.substitute(data))

    # Success report
    finalMessage = '''
Successfully created the local project {0} in {1}

To start working:

  > cd {2}
  > getpack MyPackage vXrY

then
'''

    finalMessageCMake = finalMessage + '''
  > make
  > make test
  > make QMTestSummary
  > make install

You can customize the configuration by editing the file 'CMakeLists.txt'.
'''

    finalMessageCMT = finalMessage + '''
  > . build_env.sh
  > make
  > cd MyPackage/cmt
  > cmt TestPackage
'''

    msg = use_cmake and finalMessageCMake or finalMessageCMT
    print(msg.format(opts.name, opts.user_area, devProjectDir))
