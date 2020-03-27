#!/usr/bin/env python3
import os
import sys
import json
from urllib.request import urlopen

def get_is_root() -> bool:
    return os.getuid() == 0;

def check_root() -> None:
    if get_is_root():
        pass
    else:
        print('You are not running this script as root. This means dependencies cannot be automatically installed, and a service file cannot be created.')
        carryon = input('Are you sure you wish to continue? [yN]: ')
        if carryon.lower() == 'y':
            pass
        else:
            sys.exit('Please run the script as root to continue')

def get_latest_version() -> str:
    json_data = urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json').read().decode('utf-8')
    versions = json.loads(json_data)
    return versions['latest']['release']

def main() -> None:
    print(get_latest_version())

if __name__ == '__main__':
    #check_root()
    main()
