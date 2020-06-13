from twisted.internet.protocol import Factory
from .UserHandler import UserHandler
from src.DB.DBCore import DBCore


class ServerFactory(Factory):
    def __init__(self):
        self.cursor = DBCore()
        self.authorized_users = {}

    def buildProtocol(self, addr) -> UserHandler:
        # print(f"Connected: {addr.host}:{addr.port}")
        return UserHandler(self.cursor, self.authorized_users, addr)
