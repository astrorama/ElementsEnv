'''
Common functions to add common options to a OptionParser instance.
'''

import os


class SearchPathEntry(object):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return str(self.path)


def addSearchPath(parser):
    '''
    Common options used to extend the search path.
    '''

    def dev_dir_cb(option, opt_str, value, parser):
        value = SearchPathEntry(value)
        parser.values.dev_dirs.append(value)

    parser.add_option('--dev-dir', action='callback', metavar='DEVDIR',
                      type='string', callback=dev_dir_cb,
                      help='prepend DEVDIR to the search path. '
                           'Note: the directories are searched in the '
                           'order specified on the command line.')

    parser.add_option('--user-area', action='store',
                      help='Use the specified path as User_release_area instead of '
                           'the value of the environment variable.')

    parser.add_option('--no-user-area', action='store_true',
                      help='Ignore the user release area when looking for projects.')

    parser.set_defaults(dev_dirs=[],
                        user_area=os.environ.get('User_area'),
                        no_user_area=False)

    return parser


def addOutputLevel(parser):
    '''
    Add options to get more or less messages.
    '''
    import logging
    parser.add_option('--verbose', action='store_const',
                      const=logging.INFO, dest='log_level',
                      help='print more information')
    parser.add_option('--debug', action='store_const',
                      const=logging.DEBUG, dest='log_level',
                      help='print debug messages')
    parser.add_option('--quiet', action='store_const',
                      const=logging.WARNING, dest='log_level',
                      help='print only warning messages (default)')

    parser.set_defaults(log_level=logging.WARNING)

    return parser


def addPlatform(parser):
    '''
    Add option to specify a platform.
    '''

    parser.add_option('-b', '--platform',
                      help='runtime platform [default: %default]')

    if 'BINARY_TAG' in os.environ:
        platform = os.environ['BINARY_TAG']
    else:
        # auto-detect
        from Euclid.Platform import NativeMachine
        supported = NativeMachine().supportedBinaryTag()
        if supported:
            platform = supported[0]
        else:
            parser.error(
                'unknown system, set the environment or use --platform')

    parser.set_defaults(platform=platform)

    return parser
