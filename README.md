SymSync is used to create symbolic links on a local filesystem to synchronised directories, e.g. with [Dropbox](http://www.dropbox.com).

##Config file
JSON is used to define the locations of directories and their symbolic links.
```json
[
    {
        "name": "DescriptiveName",
        "directories": {
            "origin": "E:\\Dropbox\folder",
            "symlink": "C:\\LocalFolder"
        }
    },
    {
        "name": "OtherDescriptiveName",
        "directories": {
            "origin": "E:\\Dropbox\otherfolder",
            "symlink": "C:\\otherfolder"
        }
    },
]
```