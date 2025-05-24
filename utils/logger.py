from colorama import Fore, Back, Style
from dotenv import load_dotenv
import os

load_dotenv()
LOG_FILE = os.environ.get("LOG_FILE") or False
LOG_LEVEL = os.environ.get("LOG_LEVEL") or 'INFO,WARN,ERROR'
LOG_LEVEL = LOG_LEVEL.lower().split(',')
_FILE_CREATED = "w"

LOG_FILE = LOG_FILE.lower() == "true"

def _log(message,type,error=None):
    global _FILE_CREATED

    if LOG_FILE and (type in LOG_LEVEL or "all" in LOG_LEVEL):
        with open("logs.txt", _FILE_CREATED) as myfile:
            myfile.write(f"\n{type.upper()} {message}, {error}")
        
        if _FILE_CREATED == "w": _FILE_CREATED = "a"
    
    elif (type in LOG_LEVEL or "all" in LOG_LEVEL):
        """
        TODO:
        Maybe remove any <all> reference and just do a straight check for
        levels brought by LOG_LEVEL... where <all> is the same as
        <info,debug,warn,error>
        """
    
        if type == "info" and ("all" in LOG_LEVEL or  "info" in LOG_LEVEL):
            print(f"{Fore.WHITE}{Back.GREEN}INFO{Style.RESET_ALL} {message}{Style.RESET_ALL}")
            return
        
        if type == "debug" and ("all" in LOG_LEVEL or "debug" in LOG_LEVEL):
            print(f"{Fore.WHITE}{Back.BLUE}DEBUG{Style.RESET_ALL} {message}{Style.RESET_ALL}")

        if type == "warn" and ("all" in LOG_LEVEL or "warn" in LOG_LEVEL):
            print(f"{Fore.YELLOW}{Back.LIGHTYELLOW_EX}WARN{Style.RESET_ALL} {Fore.YELLOW}{message}{Style.RESET_ALL}")
            return

        if type == "error" and ("all" in LOG_LEVEL or "error" in LOG_LEVEL):
            print(f"{Fore.YELLOW}{Back.RED}ERROR{Style.RESET_ALL} {Fore.RED}{message} -- {error}{Style.RESET_ALL}")
            return
    
    elif (LOG_LEVEL == "NONE"):
        return

def info(message):
    _log(message, "info")

def debug(message):
    _log(message, "debug")

def warn(message):
    _log(message, "warn")

def error(message, error):
    _log(message, "error", error)
    