SymSync is used to create symbolic links on a local filesystem to synchronised directories, e.g. with [Dropbox](http://www.dropbox.com).

##Usage
```
Create symbolic links to synced directories.

Usage: SymSync.py [--dry-run] CONFIG_FILE
       SymSync.py --version
       SymSync.py -h | --help

Arguments:
    CONFIG_FILE  Path to JSON configuration file

Options:
    --dry-run   Do not create symbolic links
    --version   Print version number
    -h, --help  Show this help message
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