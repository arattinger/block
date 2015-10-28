import argparse
import os
import shutil
from ast import literal_eval
from jinja2 import Template
import sys

from parsers.markdown import MarkdownParser
from parsers.restructured import RSTParser


CONTENT_PARSER = {
    "markdown": MarkdownParser,
    "restructured": RSTParser,
}

DESCRIPTION = "Block: Easily generate your static site in seconds."

settings = {
    'VERBOSE': False,
    'DEBUG': True,
}


def log(status, verbose_output=False):
    """ Simple log function that prints when the global variable VERBOSITY is
    set to True, or verbose_output=True is passed.
    """
    if verbose_output or settings['VERBOSE']:
        print(status)


def copytree1(src, dst, symlinks=False, ignore=None):
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

    try:
        copytree1(source, destination)
    except FileExistsError:
        answer = None
        while answer != 'y' and answer != 'n':
            answer = input("\nIt seems like you already have assets in "
                           "this location. \nAre you sure that you want to "
                           "override your site? [y/n] ")
        if answer == 'y':
            shutil.rmtree(destination)
            copytree1(source, destination)
        else:
            sys.exit()

    log("Finished copying files!", verbose_output=True)


def copy_static_files(source, config):
    copy_from = os.path.join(source, 'assets')
    destination = os.path.join(source, 'site/assets')

    try:
        shutil.rmtree(destination)
    except FileNotFoundError:
        # This should happen the first time we run -g as there is nothing
        # to delete yet
        pass

    copytree1(copy_from, destination)


def write_template(source, template_path, content_path, target, config):
    print("Writing", target)
    with open(os.path.join(source, template_path), 'r') as f:
        landing = f.read()

    try:
        content = CONTENT_PARSER[config['template_type']](
            os.path.join(source, content_path)).parse()
    except FileNotFoundError:
        log("Error: Please add the file: " + content_path,
            verbose_output=True)
        sys.exit()

    landing_template = Template(landing)
    landing_result = landing_template.render({
        'title': config['title'],
        'description': config['description'],
        'author': config['author'],
        'sitename': config['sitename'],
        'content': content,
        'nav_items': config['navbar'],
    })

    with open(os.path.join(source, target), 'w') as f:
        f.write(landing_result)


def write_templates(source, config):
    """ Parses the sites listed in config, opens the corresponding source
    files, and as a result creates html sites.
    """
    # 1. Write the landing page
    write_template(source, config['home']['template_path'],
                   config['home']['content_path'], 'site/index.html', config)

    # 2. Create all other pages
    for page in config['pages']:
        # An Interface change in write_template is needed to implement this
        write_template(source, page['template_path'], page['content_path'],
                       os.path.join('site', page['href']), config)


def generate_site(source):
    """ Generates the finished site from the content and assets the user specified
    """
    try:
        # We are starting by reading from main.config
        config = None
        with open(os.path.join(source, 'main.config'), 'r') as f:
            config = f.read()

        # This parsing method should be safer than a normal eval
        config = literal_eval(config)
    except:
        log('Something went wrong while parsing, please check main.config',
            verbose_output=True)
        if settings['DEBUG']:
            import traceback
            traceback.print_exc()

    log("Generating Templates...", verbose_output=True)
    # Parse landing page
    write_templates(source, config)

    log("Copying static files...", verbose_output=True)

    copy_static_files(source, config)

    log("Done generating your website!", verbose_output=True)


def main():
    args = parse_arguments()
    if args.verbose:
        settings['VERBOSE'] = True
        log("Verbose output enabled")

    if args.init:
        # Initialize the templates and folders used for the static website
        log('Attempting to create the template directories ' +
            'in the specified location',
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
