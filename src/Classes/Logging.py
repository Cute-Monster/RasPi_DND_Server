from datetime import datetime
import os

class Log:
    def __init__(self, module):
        self.error_log_file = open("{}/errors.log".format(os.path.abspath('logs')), "a")
        self.access_log_file = open("{}/access.log".format(os.path.abspath('logs')), "a")

        self.module = module

        self.priority = {
            1:"CRITICAL",
            2:"WARNING",
            3:"INFO",
            4:"DEBUG"
        }

    def log_all(self, priority, string):
        (self.access_log_file if priority == 3 or priority == 4 else self.error_log_file).writelines("{}: {}: {}: {}\n".format(
            datetime.now(),
            self.module,
            self.priority.get(priority),
            string
        ))

    def log_close(self):
        self.error_log_file.close()
        self.access_log_file.close()