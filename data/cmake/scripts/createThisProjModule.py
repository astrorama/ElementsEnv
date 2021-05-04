import os
from optparse import OptionParser


def main():
    parser = OptionParser(
        usage="ERROR: Usage %prog <project> <outputfile>")
    parser.add_option("-q", "--quiet", action="store_true",
                      help="Do not print messages.")
    opts, args = parser.parse_args()

    if len(args) != 2:
        parser.error("wrong number of arguments")

    project, outputfile = args
    if not opts.quiet:
        print("Creating %s for %s" % (outputfile, project))

    outdir = os.path.dirname(outputfile)
    if not os.path.exists(outdir):
        if not opts.quiet:
            print("Creating directory", outdir)
        os.makedirs(outdir)

    # Prepare data to be written
    outputdata = """# Automatically generated file: do not modify!

from %(proj)s_VERSION import %(proj)s_MAJOR_VERSION, %(proj)s_MINOR_VERSION, %(proj)s_PATCH_VERSION
from %(proj)s_VERSION import %(proj)s_VERSION, %(proj)s_VERSION_STRING, %(proj)s_ORIGINAL_VERSION
from %(proj)s_INSTALL import %(proj)s_INSTALL_LOCATION, %(proj)s_SEARCH_DIRS

THIS_PROJECT_ORIGINAL_VERSION = %(proj)s_ORIGINAL_VERSION
THIS_PROJECT_VCS_VERSION = %(proj)s_VCS_VERSION
THIS_PROJECT_MAJOR_VERSION = %(proj)s_MAJOR_VERSION
THIS_PROJECT_MINOR_VERSION = %(proj)s_MINOR_VERSION
THIS_PROJECT_PATCH_VERSION = %(proj)s_PATCH_VERSION
THIS_PROJECT_VERSION = %(proj)s_VERSION
THIS_PROJECT_VERSION_STRING = %(proj)s_VERSION_STRING
THIS_PROJECT_NAME = "%(Proj)s"
THIS_PROJECT_INSTALL_LOCATION = %(proj)s_INSTALL_LOCATION
THIS_PROJECT_USE_SOVERSION = %(proj)s_USE_SOVERSION
THIS_PROJECT_SEARCH_DIRS = %(proj)s_SEARCH_DIRS
""" % {'proj': project.upper(), 'Proj': project}

    # Get the current content of the destination file (if any)
    try:
        f = open(outputfile, "r")
        olddata = f.read()
        f.close()
    except IOError:
        olddata = None

    # Overwrite the file only if there are changes
    if outputdata != olddata:
        open(outputfile, "w").write(outputdata)

if __name__ == "__main__":
    main()
