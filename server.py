"""
server.py: Script that starts DND server
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.2"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru"
__status__ = "Developing"

from twisted.internet import reactor
from src.Server import ServerFactory
from src.Logging.Logger import Log

if __name__ == '__main__':
    log_file = Log(
        class_name=__name__
    )
    reactor.listenTCP(1309, ServerFactory())
    try:
        log_file.log_all(3, "Started")
        reactor.run()
    except KeyboardInterrupt as e:
        reactor.close()
        log_file.log_all(3, "Stopped")
