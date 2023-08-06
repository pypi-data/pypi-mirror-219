# Snapser CLI Tool

## Dependencies
The Snapser CLI tool depends on Python 3.X and Pip. MacOS comes pre isntalled with Python. But
please make sure you are running Python 3.X. On Windows, you can download Python 3.X from the
Windows store.

## Installation
Installing PIP on MacOS
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

Installing PIP on Windows
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Once you have Python and Pip installed
```bash
pip install --user snapctl
```
**Note** you may need to add the python path to your main $PATH variable

Verify Snapctl installation
```bash
snapctl --version
```

## Commands Help
Run the following to see the list of commands Snapser supports
```bash
snapctl --help
```

## Command - Bring your own Snap
Run the following to see the list of commands Snapser supports
```bash
snapctl byosnap publish <path_to_repo> <tag_name> <web_token>
```
