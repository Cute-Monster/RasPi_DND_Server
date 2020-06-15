"""
ServerFactory.py: Module containing factory used for twisted listenTCP method
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.2"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

from twisted.internet.protocol import Factory
from .UserHandler import UserHandler
from src.DB.DBCore import DBCore


class ServerFactory(Factory):
    """
    Module used for twisted listenTCP method as factory
    """
    def __init__(self):
        self.cursor = DBCore()
        self.authorized_users = {}

    def buildProtocol(self,
                      addr
                      ) -> UserHandler:
        """
        Create an instance of a subclass of Protocol.
        The returned instance will handle input on an incoming server
        connection, and an attribute "factory" pointing to the creating
        factory.
        :param addr: Address cortege which contains [ host, port, and connection type ]
        :return: Instance will handle input on an incoming server connection
        """

        return UserHandler(
            cursor=self.cursor,
            users=self.authorized_users,
            addr=addr
        )
