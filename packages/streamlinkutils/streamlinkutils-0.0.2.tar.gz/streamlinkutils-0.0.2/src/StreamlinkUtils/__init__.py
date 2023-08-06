"""
Module Name: Streamlink Utils
Author: Parrot Developers
Date: July 17, 2023
Description: This module adds extra utilities to Streamlink's API. I am in no way connected with streamlink.
License: MIT License
"""


import io
import os
import sys
import time
import platform
import logging
import streamlink
import subprocess
from typing import Optional
from streamlink.stream.hls import HLSStream

def dir_up(path: str) -> str:
    '''
    Returns the parent directory of the given path.

    Args:
        path (str): The path for which the parent directory will be returned.

    Returns:
        str: The parent directory of the given path.
    '''

    return os.path.dirname(path)


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


def add_pkg_folders_path(path: str) -> None:
    '''
    Adds a path to the Python system path for package folders.

    Args:
        path (str): The path to be added to the system path.

    Returns:
        None
    '''

    sys.path.append(path)


def get_cli_log() -> logging.Logger:
    '''
    Retrieves the logger for the "streamlink.cli" module.

    Returns:
        logging.Logger: The logger for the "streamlink.cli" module.
    '''

    return logging.getLogger("streamlink.cli")


def get_all_loggers() -> dict:
    '''
    Retrieves a dictionary of all loggers in the system.

    Returns:
        dict: A dictionary containing all loggers in the system.
    '''

    return logging.Logger.manager.loggerDict


def get_log_output(log: logging.Logger) -> str:
    '''
    Retrieves the output from a logger.

    Args:
        log (logging.Logger): The logger object.

    Returns:
        str: The captured log output as a string.
    '''

    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    log.addHandler(handler)

    return log_capture.getvalue()



def wait_for_stream_closing(callback, args: Optional[tuple] = (), sleep_time: Optional[int] = 5):
    '''
    Waits for the stream to be closed and then calls the callback function.

    Args:
        callback (function): The function to be called.
        args (tuple, optional): The arguments to be passed to the callback function. Defaults to ().
        sleep_time (int, optional): The time to sleep between checks. Defaults to 5.

    Returns:
        Exception or None: If an exception occurs during the callback, it is returned; otherwise, None is returned.
    '''

    cli_log = get_cli_log()
    cli_log_capture = io.StringIO()
    cli_handler = logging.StreamHandler(cli_log_capture)
    cli_log.addHandler(cli_handler)

    while True:
        cli_log_output = cli_log_capture.getvalue()
        if "Closing currently open stream" not in cli_log_output:
            time.sleep(sleep_time)
            continue

        try:
            if args:
                callback(*args)
            else:
                callback()
        except Exception as e:
            return e
        break


def wait_for_player_closed(callback, args: Optional[tuple] = (), sleep_time: Optional[int] = 5):
    '''
    Waits for the player to be closed and then calls the callback function.

    Args:
        callback (function): The function to be called.
        args (tuple, optional): The arguments to be passed to the callback function. Defaults to ().
        sleep_time (int, optional): The time to sleep between checks. Defaults to 5.

    Returns:
        Exception or None: If an exception occurs during the callback, it is returned; otherwise, None is returned.
    '''

    cli_log = get_cli_log()
    cli_log_capture = io.StringIO()
    cli_handler = logging.StreamHandler(cli_log_capture)
    cli_log.addHandler(cli_handler)

    while True:
        cli_log_output = cli_log_capture.getvalue()
        if "Player closed" not in cli_log_output:
            time.sleep(sleep_time)
            continue

        try:
            if args:
                callback(*args)
            else:
                callback()
        except Exception as e:
            return e
        break


def wait_for_stream_ended(callback, args: Optional[tuple] = (), sleep_time: Optional[int] = 5):
    '''
    Waits for the stream to end and then calls the callback function.

    Args:
        callback (function): The function to be called.
        args (tuple, optional): The arguments to be passed to the callback function. Defaults to ().
        sleep_time (int, optional): The time to sleep between checks. Defaults to 5.

    Returns:
        Exception or None: If an exception occurs during the callback, it is returned; otherwise, None is returned.
    '''

    cli_log = get_cli_log()
    cli_log_capture = io.StringIO()
    cli_handler = logging.StreamHandler(cli_log_capture)
    cli_log.addHandler(cli_handler)

    while True:
        cli_log_output = cli_log_capture.getvalue()
        if "Stream ended" not in cli_log_output:
            time.sleep(sleep_time)
            continue

        try:
            if args:
                callback(*args)
            else:
                callback()
        except Exception as e:
            return e
        break


def resolve_url(session, url, stream_type: Optional[str] ="live"):
    '''
    Resolves the URL and returns the stream variants.

    Args:
        session: The session object.
        url (str): The URL to be resolved.
        stream_type (str, optional): The type of the stream. Can be "live", "vod". Defaults to "live".

    Returns:
        dict: A dictionary containing the stream variants.
    '''

    variants = HLSStream.parse_variant_playlist(session, url)
    if not variants:
        variants = {stream_type: HLSStream(session, url)}
    return variants


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


def get_pkgs_folder() -> str:
    '''
    Retrieves the absolute path to the streamlink package folder.

    Returns:
        str: The absolute path to the streamlink package folder.
    '''

    return os.path.abspath(streamlink.__file__)



def install_pkg(pkg: str):
    '''
    Installs a package using pip into the streamlink pkgs folder.

    Args:
        pkg (str): The name of the package to install.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If the pip installation command fails.
    '''

    subprocess.check_call(["pip", "install", "--target", get_pkgs_folder(), pkg])


def get_streamlink_folder() -> str:
    '''
    Retrieves the path to the root streamlink folder.

    Returns:
        str: The path to the root streamlink folder.
    '''

    return dir_up(dir_up(dir_up(get_pkgs_folder())))