import argparse
import os
import shutil

DESCRIPTION = "Block: Easily generate your static site in seconds."

VERBOSE = False


def log(status, verbose_output=False):
    """ Simple log function that prints when the global variable VERBOSITY is
    set to True, or verbose_output=True is passed.
    """
    if verbose_output or VERBOSE:
        print(status)


def copytree(src, dst, symlinks=False, ignore=None):
    """ This is an improved implementation for copytree (shutil), and is
    used as workaround for the copytree limitation where it doesn't copy
    anything if the dir exists.

    http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def parse_arguments():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--init", help="Create a new static site",
                       metavar="absolute_path")
    group.add_argument("-g", "--generate", help="Generate the static website \
        from your source files", metavar="project_path")
    return parser.parse_args()


def copy_templates(source, destination):
    """ Copies a source directory to a destination.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)
    copytree(source, destination)


def generate_site(source):
    """ Generates the finished site from the content and assets the user specified
    """
    pass


def main():
    args = parse_arguments()
    if args.verbose:
        VERBOSE = True
        log("Verbose output enabled")

    if args.init:
        # Initialize the templates and folders used for the static website
        log('Attempting to create the template directories in the specified location',
            verbose_output=True)
        real_path = os.path.dirname(os.path.realpath(__file__))
        # print(real_path, args.init)
        copy_templates(os.path.join(real_path, 'project_template'), args.init)

    elif args.generate:
        # Generate a finished site from the content specified by the user
        generate_site(args.generate)

    log(args)
    # import pdb; pdb.set_trace()


if __name__ == '__main__':
    main()
