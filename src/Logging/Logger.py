"""
Logger.py: Module for logging server behaviour
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

# TODO reformat this class for using with builtin logger package
from datetime import datetime
import os


class Log:
    """
    Class for logging executing of the code
    """
    def __init__(self, module):
        self.log_path = os.path.abspath("Logs")
        self.error_log_file = open("{}/errors.log".format(self.log_path), "a")
        self.access_log_file = open("{}/access.log".format(self.log_path), "a")

        self.module = module

        self.priority = {
            1: "CRITICAL",
            2: "WARNING",
            3: "INFO",
            4: "DEBUG"
        }

    def log_all(self, priority: int, string):
        """
        Writing log info to files specified by priority
        :param priority: Priority of info to be logged
        :param string: Info to be writen to log file
        :return:
        """
        if self.error_log_file.closed or self.access_log_file.closed:
            self.error_log_file = open("{}/errors.log".format(self.log_path), "a")
            self.access_log_file = open("{}/access.log".format(self.log_path), "a")

        (self.access_log_file if priority == 3 or priority == 4 else self.error_log_file).writelines(
            "{} | {} | {} | {}\n".format(
                datetime.now(),
                self.module,
                self.priority.get(priority),
                string
            ))
        self.log_close()

    def log_close(self):
        """
        Closing log files
        :return:
        """
        self.error_log_file.close()
        self.access_log_file.close()
