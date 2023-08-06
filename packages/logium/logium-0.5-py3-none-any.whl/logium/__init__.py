"""
A simple logging library for recording and displaying log messages.

Author: N0rmalUser
Version: 0.5

This library provides a Logger class that allows you to log messages with various severity levels. The log messages can be output to the console and/or saved to a log file with timestamps.

Usage:
1. Create an instance of the Logger class by providing the log file name and optional settings.
2. Use the logger instance to call different logging methods based on the severity level.
3. The log messages will be printed to the console and/or appended to the log file.

Classes:
- logger: Class for logging and recording logs.
- help: Provides detailed information about the methods of the Logger class.

Methods:
- Logger.__init__(self, *file: str, console_enabled=True, datetime_format='%d.%m.%Y %H:%M:%S',
                   date_in_console=True, file_enable=True, date_in_file=True):
    Initializes an instance of the Logger class.
    Args:
        file (str): The name of the log file.
        console_enabled (bool): Whether logging is enabled in the console (default: True).
        datetime_format (str): The format of the date and time for the logs (default: '%d.%m.%Y %H:%M:%S').
        date_in_console (bool): Whether to include date and time in the console output (default: True).
        file_enable (bool): Whether to enable log file writing (default: True).
        date_in_file (bool): Whether to include date and time in the file output (default: True).

- Logger.d(self) -> None:
    Method for debug messages.

- Logger.e(self) -> None:
    Method for error messages.

- Logger.i(self) -> None:
    Method for informational messages.

- Logger.s(self) -> None:
    Method for settings messages.

- Logger.w(self) -> None:
    Method for warning messages.

- Logger.c(self) -> None:
    Method for critical messages.

Example Usage:
```python
from logium import logger

# Create an instance of the Logger
my_logger = logger('log.txt')

# Log messages
my_logger.d('This is a debug message')
my_logger.e('This is an error message')
my_logger.i('This is an informational message')
my_logger.s('This is a settings message')
my_logger.w('This is a warning message')
my_logger.c('This is a critical message')
```
"""
from datetime import datetime


def _printer(self):
    """
    The inner function for printing the message to the console and/or file
    """
    if self.console_enabled:
        print(f'{self.time} {self.message}' if self.console_enabled and self.date_in_console else self.message)
    if self.file_enable:
        with open(self.file[0], "a", encoding='utf-8') as f:
            f.write(f'{self.time} {self.message}\n' if self.file_enable and self.date_in_file else self.message)


def _tagger(func):
    """
    The inner decorator function tagger takes a function and adds a tag to the message.
    """
    def wrapper(self, *args):
        message = ' '.join(str(arg) + (':' if i != len(args) - 1 else '') for i, arg in enumerate(args))
        self.message = message
        return func(self)

    return wrapper


class logger:
    """
    Class for logging and recording logs
    """

    def __init__(self, *file: str, console_enabled=True, datetime_format='%d.%m.%Y %H:%M:%S',
                 date_in_console=True, file_enable=True, date_in_file=True):
        """
        Initializes an instance of the logger class.

        Args:
            file (str): The name of the log file.
            console_enabled (bool): Whether logging is enabled in the console (default: True).
            datetime_format (str): The format of the date and time for the logs (default: '%d.%m.%Y %H:%M:%S').
            date_in_console (bool): Whether to include date and time in the console output (default: True).
            file_enable (bool): Whether to enable log file writing (default: True).
            date_in_file (bool): Whether to include date and time in the file output (default: True).
        """
        if not all(isinstance(var, bool) for var in (console_enabled, date_in_console, file_enable, date_in_file)):
            raise ValueError("console_enabled, date_in_console, date_in_file, and file_enabled must be of bool type")
        if not all(isinstance(file, str) for file in file):
            raise ValueError("logfiles must be of str type")
        if not isinstance(datetime_format, str):
            raise ValueError("datetime_format must be of str type")
        self.file = file
        self.time = datetime.now().strftime(datetime_format)
        self.console_enabled = console_enabled
        self.file_enable = file_enable
        self.date_in_console = date_in_console
        self.date_in_file = date_in_file
        self.message = ''

    @_tagger  # debug
    def d(self) -> None:
        """
        Decorator method for debug messages
        """
        self.message = '-DEBUG-' + self.message
        _printer(self)

    @_tagger  # error
    def e(self) -> None:
        """
        Decorator method for error messages
        """
        self.message = '-ERROR- ' + self.message
        _printer(self)

    @_tagger  # info
    def i(self) -> None:
        """
        Decorator method for informational messages
        """
        self.message = '-INFO- ' + self.message
        _printer(self)

    @_tagger  # settings
    def s(self) -> None:
        """
        Decorator method for settings messages
        """
        self.message = '-SETTINGS-' + self.message
        _printer(self)

    @_tagger  # warning
    def w(self) -> None:
        """
        Decorator method for warning messages
        """
        self.message = '-WARNING- ' + self.message
        _printer(self)

    @_tagger  # critical
    def c(self) -> None:
        """
        Decorator method for critical messages
        """
        self.message = '-CRITICAL- ' + self.message
        _printer(self)
