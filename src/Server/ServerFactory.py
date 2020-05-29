from twisted.internet.protocol import Factory
from .Server import Server


class ServerFactory(Factory):
    def __init__(self):
        self.authorized_users = {}

    def buildProtocol(self, addr) -> Server:
        print(f"Connected: {addr.host}:{addr.port}")
        return Server(self.authorized_users, addr)