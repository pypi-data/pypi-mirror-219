"""This logger is used to log the request information of the yellowdot project in the CLI."""
from colorama import Fore, Style


class YDLogger(object):
    context = ""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(YDLogger, cls).__new__(cls)
        return cls._instance

    # Returns the single instance of the YDLogger class.
    @staticmethod
    def get_instance():
        if not YDLogger._instance:
            YDLogger._instance = YDLogger(YDLogger.context)
        return YDLogger._instance

    # Initializes the parameters.
    def __init__(self, context: str):
        self.context = context

    # Logs info messages on the console.
    def info(self, message: str):
        print(f"{Fore.GREEN}[INFO]: [{self.context}] {Style.RESET_ALL}{message}\n")

    # Logs error messages on the console.
    def error(self, message: str):
        print(f"{Fore.RED}[ERROR]: [{self.context}] {Style.RESET_ALL}{message}\n")

    # Logs warning messages on the console.
    def warning(self, message: str):
        print(f"{Fore.YELLOW}[WARNING]: [{self.context}] {Style.RESET_ALL}{message}\n")

    # Logs success messages on the console.
    def success(self, message: str):
        print(f"{Fore.GREEN}[SUCCESS]: [{self.context}] {Style.RESET_ALL}{message}\n")

    # Logs debug messages on the console.
    def debug(self, message: str):
        print(f"{Fore.BLUE}[DEBUG]: [{self.context}] {Style.RESET_ALL}{message}\n")

    # Logs the message on the console with the given color.
    def log(self, message: str, color: str):
        print(f"{color}[LOG]: [{self.context}] {Style.RESET_ALL}{message}\n")

    # Logs WTF messages on the console.
    def wtf(self, message: str):
        print(f"{Fore.RED}[WTF]: [{self.context}] {Style.RESET_ALL}{message}\n")
