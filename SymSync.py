#!python3
import argparse
import ctypes
import json
import os
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


parser = argparse.ArgumentParser()
parser.add_argument('config_file', help='Path to JSON configuration file')
parser.add_argument('--dry-run', action='store_true', help='Do not create symbolic links')
args = parser.parse_args()

if args.dry_run:
    print('***** Dry Run *****\n')

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
        print('Origin folder "{0}" does not exist, check config.'.format(origin))
        exit()

    if os.path.exists(symlink):
        if isDirReparsePoint(symlink):
            print('Already a symbolic link, skipping. "{0}"'.format(symlink))
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


confFile.close()
