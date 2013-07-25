#!python3
"""Create symbolic links to synced directories.

Usage: SymSync.py [--dry-run] CONFIG_FILE
       SymSync.py --version
       SymSync.py -h | --help

Arguments:
    CONFIG_FILE  Path to JSON configuration file

Options:
    --dry-run   Do not create symbolic links
    --version   Print version number
    -h, --help  Show this help message
"""
from docopt import docopt
import json
import os
import shutil
import sys
import win32con
import win32file


def isDirReparsePoint(dir):
    '''Determines if directory is a symbolic link.'''
    if not os.path.exists(dir):
        raise FileNotFoundError
    attr = win32file.GetFileAttributes(dir)
    if not (attr & win32con.FILE_ATTRIBUTE_DIRECTORY):
        raise TypeError('"{0}" is not a directory'.format(dir))
    return bool(attr & win32con.FILE_ATTRIBUTE_REPARSE_POINT)

version = '1.2'

args = docopt(__doc__, version=version)

if args['--dry-run']:
    print('***** Dry Run *****\n')

try:
    confFile = open(args['CONFIG_FILE'])
    conf = json.load(confFile)
except ValueError as err:
    print('Error loading config file:\n{0}'.format(err))
    sys.exit()
except FileNotFoundError:
    print('Config file does not exist.')
    sys.exit()


for item in conf:
    origin = item['directories']['origin']
    symlink = item['directories']['symlink']
    if not os.path.exists(origin):
        # If origin doesn't exist, but a directory at the location of symlink
        # does, move those files to origin and create the symlink.
        if os.path.exists(symlink) and not isDirReparsePoint(symlink):
            if args['--dry-run']:
                print('Move existing folder. ("{0}" to "{1}")'.format(
                    symlink, origin))
            else:
                shutil.move(symlink, origin)
                print('Moving existing folder. ("{0}" moved to "{1}")'.format(
                    symlink, origin))

    if os.path.exists(symlink):
        if isDirReparsePoint(symlink):
            print('Already a symbolic link, skipping. ("{0}")'.format(symlink))
        else:
            print('Existing directory, skipping. "{0}"'.format(symlink))
    else:
        try:
            if args['--dry-run']:
                print('Create symbolic link, "{0}" -> "{1}"'.format(
                    symlink, origin))
            else:
                win32file.CreateSymbolicLink(
                    symlink, origin, win32file.SYMBOLIC_LINK_FLAG_DIRECTORY)
                if isDirReparsePoint(symlink):
                    print('Symbolic link created successfully, '
                          '"{0}" -> "{1}"'.format(symlink, origin))
                else:
                    print('Symbolic link not created for unknown reason. '
                          '"{0}" -> "{1}"'.format(symlink, origin))
        except Exception as err:
            print('Unknown error: {0}'.format(err))


confFile.close()
