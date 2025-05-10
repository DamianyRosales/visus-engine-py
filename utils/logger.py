from colorama import Fore, Back, Style
from dotenv import load_dotenv
import os

load_dotenv()
LOG_FILE = os.environ.get("LOG_FILE") or False
LOG_LEVEL = os.environ.get("LOG_LEVEL") or 'ALL'
_FILE_CREATED = "w"

LOG_FILE = LOG_FILE.lower() == "true"

def _log(message,type,error=None):
    global _FILE_CREATED

    if LOG_FILE and (LOG_LEVEL == type or LOG_LEVEL == "ALL"):
        with open("logs.txt", _FILE_CREATED) as myfile:
            myfile.write(f"\n{type.upper()} {message}, {error}")
        
        if _FILE_CREATED == "w": _FILE_CREATED = "a"

    else:
        
        if type == "info" and (LOG_LEVEL == "ALL" or LOG_LEVEL == "info"):
            print(f"{Fore.WHITE}{Back.GREEN}INFO{Style.RESET_ALL} {message}{Style.RESET_ALL}")
            return

        if type == "warn" and (LOG_LEVEL == "ALL" or LOG_LEVEL == "warn"):
            print(f"{Fore.YELLOW}{Back.LIGHTYELLOW_EX}WARN{Style.RESET_ALL} {Fore.YELLOW}{message}{Style.RESET_ALL}")
            return

        if type == "error" and (LOG_LEVEL == "ALL" or LOG_LEVEL == "error"):
            print(f"{Fore.YELLOW}{Back.RED}ERROR{Style.RESET_ALL} {Fore.RED}{message} -- {error}{Style.RESET_ALL}")
            return

def info(message):
    _log(message, "info")

def warn(message):
    _log(message, "warn")

def error(message, error):
    _log(message, "error", error)
    