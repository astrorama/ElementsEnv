
import sys
import logging


def run(cmd):
    # Prepare the profiler instance
    profiler = None
    try:
        import cProfile
        profiler = cProfile.Profile()
    except ImportError:
        try:
            import profile
            profiler = profile.Profile()
        except ImportError:
            logging.warning(
                'Cannot import cProfile or profile: ignoring --profile')
            exec(cmd)
    try:
        # if we managed to get the profiler instance, collect profiling stats,
        # and print them on stderr
        profiler.run(cmd)

    except SystemExit:  # intercept normal exit
        # adapted from Python standard profiler.py
        import pstats
        stream = sys.stderr
        stream.write('\n')
        stream.write('{0:=^80}\n\n'.format(' profiling results '))
        stats = pstats.Stats(profiler, stream=stream)
        stats.strip_dirs().sort_stats('cumulative').print_stats(10)
        stream.write((80 * '=') + '\n')

        # propagate return code
        raise
