"""
Logger.py: Module for logging server behaviour into specific log files
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

    def __init__(self,
                 class_name
                 ):
        self.log_path = os.path.abspath("Logs")
        self.class_name = class_name
        self.priority = {
            1: "CRITICAL",
            2: "WARNING",
            3: "INFO",
            4: "DEBUG"
        }

    def log_all(self,
                priority: int,
                string: str
                ):
        """
        Writing log info to files specified by priority
        :param priority: Priority of info to be logged
        :param string: Info to be written to log file
        :return:
        """

        with open("{}/{}.log".format(
                self.log_path,
                "access" if priority == 3 or priority == 4 else "errors"
        ),
                "a") as f:
            f.writelines(
                "{} | {} | {} | {}\n".format(
                    datetime.now(),
                    self.class_name,
                    self.priority.get(priority),
                    string
                )
            )
