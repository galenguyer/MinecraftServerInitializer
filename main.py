#!/usr/bin/env python3
import os
import sys

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

def main() -> None:
    pass

if __name__ == '__main__':
    check_root()
    main()
