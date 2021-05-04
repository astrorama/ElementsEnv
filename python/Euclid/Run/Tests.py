
import os
import sys
from tempfile import mkdtemp
import shutil

latest_gaudi = 'v23r7'


def prepare_tree(base, tree):
    from os import makedirs
    from os.path import dirname, join, exists
    if hasattr(tree, 'items'):
        tree = tree.items()
    for k, v in tree:
        k = join(base, k)
        if v:
            d = dirname(k)
            if not exists(d):
                makedirs(d)
            f = open(k, 'w')
            f.write(v)
            f.close()
        else:
            if not exists(k):
                makedirs(k)


class TempDir(object):

    def __init__(self, tree=None):
        self.tmpdir = None
        self.tree = tree

    def __enter__(self):
        self.tmpdir = mkdtemp()
        if self.tree:
            prepare_tree(self.tmpdir, self.tree)
        return self.tmpdir

    def __exit__(self, type_, value, traceback):
        if self.tmpdir:
            shutil.rmtree(self.tmpdir)


def test_import():
    import Euclid.Run
    assert Euclid.Run.path


def test_version():
    from Euclid.Run.Version import expandVersionAlias, isValidVersion

    # this is a dummy test, waiting for a real implementation of version
    # aliases
    assert expandVersionAlias('Gaudi', 'latest') == 'latest'

    assert isValidVersion('Gaudi', 'latest')
    assert isValidVersion('Gaudi', 'HEAD')
    assert isValidVersion('Gaudi', latest_gaudi)
    assert isValidVersion('LHCb', 'v32r5p1')
    assert isValidVersion('LHCb', 'v32r4g1')
    assert not isValidVersion('Gaudi', 'a random string')


def parse_args(func, args):
    from optparse import OptionParser
    return func(OptionParser(prog='dummy_program')).parse_args(args)


def test_options_addOutputLevel():
    from Euclid.Run.Options import addOutputLevel
    import logging

    opts, _ = parse_args(addOutputLevel, [])
    assert opts.log_level == logging.WARNING

    opts, _ = parse_args(addOutputLevel, ['--debug'])
    assert opts.log_level == logging.DEBUG

    opts, _ = parse_args(addOutputLevel, ['--verbose'])
    assert opts.log_level == logging.INFO

    opts, _ = parse_args(addOutputLevel, ['--quiet'])
    assert opts.log_level == logging.WARNING


def test_options_addPlatform():
    from Euclid.Run.Options import addPlatform

    opts, _ = parse_args(addPlatform, ['-c', 'platform1'])
    assert opts.platform == 'platform1'

    opts, _ = parse_args(addPlatform, ['--platform', 'platform2'])
    assert opts.platform == 'platform2'

    if 'CMTCONFIG' not in os.environ:
        os.environ['CMTCONFIG'] = 'default'
    if 'BINARY_TAG' in os.environ:
        del os.environ['BINARY_TAG']
    opts, _ = parse_args(addPlatform, [])
    assert opts.platform == os.environ['CMTCONFIG']

    os.environ['BINARY_TAG'] = 'another'
    opts, _ = parse_args(addPlatform, [])
    assert opts.platform == os.environ['BINARY_TAG']
    del os.environ['BINARY_TAG']

    del os.environ['CMTCONFIG']
    opts, _ = parse_args(addPlatform, [])
    assert opts.platform

    import Euclid.Platform
    bk = Euclid.Platform.NativeMachine

    class dummy():

        def CMTSupportedConfig(self):
            return None
    Euclid.Platform.NativeMachine = dummy
    try:
        opts, _ = parse_args(addPlatform, [])
        assert False, 'exception expected'
    except SystemExit:
        pass
    Euclid.Platform.NativeMachine = bk


def test_options_addSearchPath():
    from Euclid.Run.Options import addSearchPath

    if 'LHCBDEV' not in os.environ:
        os.environ['LHCBDEV'] = '/afs/cern.ch/lhcb/software/DEV'
    opts, _ = parse_args(addSearchPath, ['--dev'])
    assert os.environ['LHCBDEV'] in map(str, opts.dev_dirs)

    del os.environ['LHCBDEV']
    try:
        opts, _ = parse_args(addSearchPath, ['--dev'])
        assert False, 'exception expected'
    except SystemExit:
        pass

    opts, _ = parse_args(addSearchPath, ['--dev-dir', '/some/path'])
    assert '/some/path' in map(str, opts.dev_dirs)

    if 'User_release_area' in os.environ:
        del os.environ['User_release_area']
    opts, _ = parse_args(addSearchPath, [])
    assert opts.user_area is None

    os.environ['User_release_area'] = '/home/myself/cmtuser'
    opts, _ = parse_args(addSearchPath, [])
    assert opts.user_area == os.environ['User_release_area']
    assert not opts.no_user_area

    opts, _ = parse_args(addSearchPath, ['--user-area', '/tmp/myself'])
    assert opts.user_area == '/tmp/myself'

    opts, _ = parse_args(addSearchPath, ['--no-user-area'])
    assert opts.no_user_area

    try:
        opts, _ = parse_args(addSearchPath, ['--nightly'])
        assert False, 'exception expected'
    except SystemExit:
        pass

    import datetime
    days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    weekday = datetime.date.today().weekday()
    today = days[weekday]
    yesterday = days[(weekday - 1) % 7]

    with TempDir({'lhcb-nightly-slot/%s' % today: None,
                  'lhcb-nightly-slot/%s' % yesterday: None}) as tmp:
        os.environ['LHCBNIGHTLIES'] = tmp
        opts, _ = parse_args(addSearchPath, ['--nightly', 'lhcb-nightly-slot'])
        assert os.path.join(
            tmp, 'lhcb-nightly-slot', today) in map(str, opts.dev_dirs)
        assert opts.nightly == ('lhcb-nightly-slot', today)
        opts, _ = parse_args(
            addSearchPath, ['--nightly', 'lhcb-nightly-slot', yesterday])
        assert os.path.join(
            tmp, 'lhcb-nightly-slot', yesterday) in map(str, opts.dev_dirs)
        assert opts.nightly == ('lhcb-nightly-slot', yesterday)

        try:
            opts, _ = parse_args(addSearchPath, ['--nightly', 'dummy'])
            assert False, 'exception expected'
        except SystemExit:
            pass

        try:
            opts, _ = parse_args(addSearchPath, ['--nightly', 'lhcb-nightly-slot',
                                                 days[(weekday + 1) % 7]])
            assert False, 'exception expected'
        except SystemExit:
            pass

    with TempDir({'lhcb-nightly-slot/%s/confSummary.py' % today: '''cmtProjectPathList = ['/extra/dir']\n'''}) as tmp:
        os.environ['LHCBNIGHTLIES'] = tmp
        opts, _ = parse_args(addSearchPath, ['--nightly', 'lhcb-nightly-slot'])
        assert '/extra/dir' in map(str, opts.dev_dirs)

    with TempDir({'lhcb-nightly-slot/%s/configuration.xml' % today: '''<configuration><slot name="lhcb-nightly-slot">
<cmtprojectpath><path value="/extra/xml/dir"/></cmtprojectpath>
</slot></configuration>'''}) as tmp:
        os.environ['LHCBNIGHTLIES'] = tmp
        opts, _ = parse_args(addSearchPath, ['--nightly', 'lhcb-nightly-slot'])
        assert '/extra/xml/dir' in map(str, opts.dev_dirs)


def test_profiling():
    from Euclid.Run import Profiling

    from StringIO import StringIO

    try:
        sys.stderr = StringIO()
        Profiling.run('sys.exit()')
        assert False, 'exception expected'
    except SystemExit:
        print(sys.stderr.getvalue())
    finally:
        sys.stderr = sys.__stderr__

    def dummy():
        raise ImportError()

    import cProfile
    bk1 = cProfile.Profile
    cProfile.Profile = dummy

    try:
        sys.stderr = StringIO()
        Profiling.run('sys.exit()')
        assert False, 'exception expected'
    except SystemExit:
        print(sys.stderr.getvalue())
    finally:
        sys.stderr = sys.__stderr__

    import profile
    bk2 = profile.Profile
    profile.Profile = dummy
    try:
        sys.stderr = StringIO()
        Profiling.run('sys.exit()')
        assert False, 'exception expected'
    except SystemExit:
        print(sys.stderr.getvalue())
    finally:
        sys.stderr = sys.__stderr__

    cProfile.Profile = bk1
    profile.Profile = bk2
