block
=====

A python 3 static site generator.


Usage:
------

### Creating the initial demo site

Start by initiating a new site:

python block.py --init [ absolute_path ]

The newly created directory contains all the files you need to get started.

### Edit the files

There are 3 parts of a newly created project that can/should be edited:

#### main.config

Block knows where to find things by reading from the main.config. 
The probably most important parts are the "home" and the "pages" 
sections which define what pages should be created!

#### The content directory

The content directory defines the things that will be displayed to a user. 
Every page defined in main.config needs a content file to work. 
Block supports two standards: Markdown and RestructuredText.

#### The assets directory

This contains all the scripts and css files that are used in the static site.
All changes are copied over to the finished site.

### Generate your static sites

python block.py --generate [ project_path ]

This will parse all content files and copy the finished result to the site folder. 
Note: Never edit anything in the site folder, as it will be replaced by the newly created copy!



Arguments:
----------

usage: block.py [-h] [-v] [-i absolute_path | -g project_path]

Block: Easily generate your static site in seconds.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -i absolute_path, --init absolute_path
                        Create a new static site
  -g project_path, --generate project_path
                        Generate the static website from your source files

