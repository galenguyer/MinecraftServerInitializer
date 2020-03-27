#!/usr/bin/env python3
import os

def get_is_root() -> bool:
    return os.getuid() == 0;

def main():
    pass

if __name__ == '__main__':
    main()
