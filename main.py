#!/usr/bin/env python3
import os
import sys
import time
import json
from urllib.request import urlopen, urlretrieve


MC_VERSIONS = json.loads(urlopen('https://launchermeta.mojang.com/mc/game/version_manifest.json').read().decode('utf-8'))
USER_VERSION = 'latest'
FILE_PATH = os.getcwd()
MEM_SIZE = min(((os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'))/(1024.**3)), 4)

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = min(int(count*block_size*100/total_size),100)
    sys.stdout.write("\r%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


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
    global MC_VERSIONS
    return MC_VERSIONS['latest']['release']


def get_vanilla_url(selected: str):
    global MC_VERSIONS
    for version in MC_VERSIONS['versions']:
        if version['id'] == selected:
            version_json = json.loads(urlopen(version['url']).read().decode('utf-8'))
            return version_json['downloads']['server']['url']
    (f'Invalid version {selected}. Exiting')


def download_server(url: str):
    global FILE_PATH
    global USER_VERSION
    path = input(f"Where would you like file saved? The default is the current directory ({os.getcwd()})")
    if path:
        FILE_PATH = path
    if FILE_PATH[-1] != '/':
        FILE_PATH += '/'
    if os.path.exists(FILE_PATH) or os.access(os.path.dirname(FILE_PATH), os.W_OK):
        urlretrieve(url, f"{FILE_PATH}minecraft-server-{USER_VERSION}.jar", reporthook)
        time.sleep(0.5)
        print(f"\nDownloaded minecraft-server-{USER_VERSION}.jar to {FILE_PATH}")
    else:
        sys.exit(f"'{FILE_PATH}' is not a valid or writeable path")



def finish():
    global MEM_SIZE
    server_name = FILE_PATH.strip('/').split('/')[-1]
    print("\nDone!")
    print(f"If you opted to create a systemd service, start the server by running 'systemctl start {server_name}' as root")
    print(f"Otherwise, run it with 'java -jar -Xms{MEM_SIZE}G -Xmx{MEM_SIZE}G minecraft-server-{USER_VERSION}.jar nogui'. The -Xm options refer to \
minimum and maximum memory allocated to the JVM. Only edit these if you experience performance issues and you know what you're doing.")
    exit(0)


def create_systemd_file():
    print("Haha not yet")


def main() -> None:
    global USER_VERSION
    uver = input(f'What version of Minecraft would you like? The default is the lateset release ({get_latest_version()}): ')
    if uver:
        USER_VERSION = uver.lower()
    else:
        USER_VERSION = get_latest_version()
    download_server(get_vanilla_url(USER_VERSION))
    
    create_systemd = input('Do you want a systemd unit to be created? [Yn]: ')
    if create_systemd.lower() != 'n':
        create_systemd_file()
    finish()

if __name__ == '__main__':
    #check_root()
    main()
