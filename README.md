SymSync is used to create symbolic links on a local filesystem to synchronised directories, e.g. with [Dropbox](http://www.dropbox.com).

##Usage
```
usage: SymSync.py [-h] [--version] [--dry-run] config_file

Create symbolic links to synced directories.

positional arguments:
  config_file    Path to JSON configuration file

optional arguments:
  -h, --help     show this help message and exit
  --version, -v  show program's version number and exit
  --dry-run      Do not create symbolic links
```

##Config file
JSON is used to define the locations of directories and their symbolic links.
```json
[
    {
        "name": "DescriptiveName",
        "directories": {
            "origin": "E:\\Dropbox\\folder",
            "symlink": "C:\\LocalFolder"
        }
    },
    {
        "name": "OtherDescriptiveName",
        "directories": {
            "origin": "E:\\Dropbox\\otherfolder",
            "symlink": "C:\\otherfolder"
        }
    },
]
```