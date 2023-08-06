import os
from colorama import init
from colorama import Fore, Back, Style
from datetime import datetime

__all__ = ['log_info', 'log_warn', 'log_error', 'log_end', 'format_capacity']
init()


def get_time():
    return datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')


def format_capacity(buffer):
    size = len(buffer)
    if size > 1024:
        return f'{size/1024:.2F} KB'
    else:
        return f'{size/1024/1024:.2f} MB'


def log_end(end):
    if end:
        separator = '-' * os.get_terminal_size().columns
        print(separator+'\n\n')


def log_info(message, end=False):
    message = f"[{get_time()}]: {message}"
    print(Fore.BLACK, Back.WHITE, '[ INFO]-'+message)
    print(Style.RESET_ALL)
    log_end(end)


def log_warn(message, end=False):
    message = f"[{get_time()}]: {message}"
    print(Fore.CYAN, Back.YELLOW, '[ WARN]-'+message)
    print(Style.RESET_ALL)
    log_end(end)


def log_error(message, error=None, end=False):
    message = f"[{get_time()}]: {message}"
    print(Fore.CYAN, Back.RED, '[ERROR]-'+message)

    if error:
        print(error)

    print(Style.RESET_ALL)
    log_end(end)
