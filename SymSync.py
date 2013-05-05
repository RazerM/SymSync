#!python3
import argparse
import ctypes
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

version = '1.0'

parser = argparse.ArgumentParser(description='Create symbolic links to synced directories.')
parser.add_argument('--version', '-v', action='version', version='%(prog)s {0}'.format(version))
parser.add_argument('config_file', help='Path to JSON configuration file')
parser.add_argument('--dry-run', action='store_true', help='Do not create symbolic links')
args = parser.parse_args()

if args.dry_run:
    print('***** Dry Run *****\n')
else:
    print('***** SymSync *****\n')

try:
    confFile = open(args.config_file)
    conf = json.load(confFile)
except ValueError as err:
    print('Error loading config file:\n{0}'.format(err))
    exit()
except FileNotFoundError:
    print('Config file does not exist.')
    exit()


for item in conf:
    origin = item['directories']['origin']
    symlink = item['directories']['symlink']
    if not os.path.exists(origin):
        # If origin doesn't exist, but a directory at the location of symlink does,
        # move those files to origin and create the symlink.
        if os.path.exists(symlink) and not isDirReparsePoint(symlink):
            shutil.move(symlink, origin)
            print('Moving existing folder. ("{0}" moved to "{1}")'.format(symlink, origin))

    if os.path.exists(symlink):
        if isDirReparsePoint(symlink):
            print('Already a symbolic link, skipping. ("{0}")'.format(symlink))
        else:
            print('Existing directory, skipping. "{0}"'.format(symlink))
    else:
        try:
            if args.dry_run:
                print('Create symbolic link, "{0}" -> "{1}"'.format(symlink, origin))
            else:
                win32file.CreateSymbolicLink(symlink, origin, win32file.SYMBOLIC_LINK_FLAG_DIRECTORY)
                if isDirReparsePoint(symlink):
                    print('Symbolic link created successfully, "{0}" -> "{1}"'.format(symlink, origin))
                else:
                    print('Symbolic link not created for unknown reason. "{0}" -> "{1}"'.format(symlink, origin))
        except Exception as err:
            print('Unknown error: {0}'.format(err))
    print('\n')


confFile.close()
