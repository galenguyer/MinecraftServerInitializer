#!/usr/bin/env python3
import os
import sys
import json
from urllib.request import urlopen

MC_VERSIONS = json.loads(urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json').read().decode('utf-8'))
USER_VERSION = 'latest'

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
    return MC_VERSIONS['latest']['release']

def get_vanilla_url(selected: str):
    for version in MC_VERSIONS['versions']:
        if version['id'] == selected:
            version_json = json.loads(urlopen(version['url']).read().decode('utf-8'))
            return version_json['downloads']['server']['url']
    sys.exit(f'Invalid version {selected}. Exiting')

def main() -> None:
    uver = input(f'Input the version of Minecraft to use. The default is the lateset release ({get_latest_version()}): ')
    if uver:
        USER_VERSION = uver.lower()
    else:
        USER_VERSION = get_latest_version()
    print(get_vanilla_url(USER_VERSION))

if __name__ == '__main__':
    #check_root()
    main()
