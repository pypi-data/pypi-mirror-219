import os
import platform
import requests
from tqdm import tqdm
from typing import Optional
from colorama import Fore, Style


def detect_os() -> str:
    '''
    Detects the operating system and returns its name.

    Returns:
        str: The name of the detected operating system.
    '''

    system = platform.system()
    
    if system == 'Darwin':
        return 'macOS'
    elif system == 'Windows':
        return 'Windows'
    elif system == 'Linux':
        return 'Linux'
    else:
        return 'Unknown'
    

def clear_console():
    os_name = platform.system().lower()
    if os_name.startswith('win'):
        os.system('cls')
    elif os_name.startswith('linux') or os_name.startswith('darwin'):
        os.system('clear')
    else:
        print("Unsupported operating system. Unable to clear console.")


def get_appdata() -> str:
    '''
    Retrieves the path to the APPDATA directory.

    Returns:
        str: The path to the APPDATA directory.
    '''

    return os.environ['APPDATA']


def get_home() -> str:
    '''
    Retrieves the path to the user's home directory.

    Returns:
        str: The path to the user's home directory.
    '''

    return os.getenv('HOME')


def xdg_config_home() -> str:
    '''
    Retrieves the path to the XDG_CONFIG_HOME directory.

    Returns:
        str: The path to the XDG_CONFIG_HOME directory.
    '''

    return os.getenv('XDG_CONFIG_HOME', os.path.join(get_home(), '.config'))


def xdg_data_home() -> str:
    '''
    Retrieves the path to the XDG_DATA_HOME directory.

    Returns:
        str: The path to the XDG_DATA_HOME directory.
    '''

    return os.getenv('XDG_DATA_HOME', os.path.join(os.getenv('HOME'), '.local', 'share'))


def get_plugins_folder(custom_os: Optional[str] = detect_os(), deprecated: bool = False) -> str:
    '''
    Retrieves the path to the plugins folder based on the operating system.

    Args:
        custom_os (str, optional): The custom operating system. Defaults to the detected operating system.
        deprecated (bool, optional): Flag indicating whether the deprecated plugins folder should be used. Defaults to False.

    Returns:
        str: The path to the plugins folder.
    
    Raises:
        Exception: If the operating system is unknown.
    '''

    if custom_os == "Windows":
        return os.path.join(get_appdata(), "streamlink", "plugins")
    
    elif custom_os == "macOS":
        if deprecated:
            return os.path.join(xdg_config_home(), 'streamlink', 'plugins')
        return os.path.join(get_home(), 'Library', 'Application Support', 'streamlink', 'plugins')
    
    elif custom_os == "Linux":
        if deprecated:
            return os.path.join(xdg_config_home(), 'streamlink', 'plugins')
        return os.path.join(xdg_data_home(), 'streamlink', 'plugins')
    
    else:
        raise Exception("Unknown OS")
    

def download_file(url, destination):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    with open(destination, 'wb') as file:
        with tqdm(total=total_size, unit='iB', unit_scale=True,
                  bar_format=Fore.RED+"{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}",

                  ncols=80) as progress_bar:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar.update(len(data))

                progress = progress_bar.n / progress_bar.total
                #color_code = Fore.GREEN if progress >= 1.0 else Fore.RED
                progress_bar.set_postfix_str(f"{progress_bar.n / 1024:.2f} KiB{Style.RESET_ALL}")




banner_ = Fore.RED+""" #####   ####              ######   #######  ######    #####              ####   ####      ######  
##   ##   ##                ##  ##   ##   #   ##  ##  ### ###            ##  ##   ##         ##    
##        ##                ##  ##   ##       ##  ##  ##   ##           ##        ##         ##    
 #####    ##                #####    ####     #####   ##   ##           ##        ##         ##    
     ##   ##                ## ##    ##       ##      ##   ##           ##        ##         ##    
##   ##   ##  ##            ## ##    ##   #   ##      ### ###            ##  ##   ##  ##     ##    
 #####   #######           #### ##  #######  ####      #####              ####   #######   ######"""+Fore.WHITE

def banner():
    print(banner_+("\n"*1))