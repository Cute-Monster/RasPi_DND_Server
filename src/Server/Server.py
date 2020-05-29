"""
Server.py: Main module of server/Heart of the server
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghosatshow@yandex.ru "
__status__ = "Developing"

import json
from abc import ABC
from typing import Any
from pprint import pprint

from twisted.protocols.basic import LineReceiver
from src.Logging.Logger import Log
from src.Modules import UtilityModule, UserModule, DungeonSkeleton
from src import CustomExceptions
from src.DB.DBCore import DBCore


__all__ = ["Server"]


class Server(LineReceiver, ABC):
    """
    Heart of the server
    """
    def __init__(self, authorized_users, addr):
        self.cursor = DBCore()
        self.dungeon_generator = DungeonSkeleton(self.cursor)
        self.authorized_users = authorized_users
        self.addr = addr
        self.identify = str(addr.host) + ':' + str(addr.port)
        self.player = None
        self.log_file = Log(self.__module__)
        self.actions = {
            "playerRegistration": self.player_registration,
            "playerAuthorization": self.player_authorization,
            "sendChatMessage": self.send_chat_message,
            "sendPrivateMessage": self.send_private_message,
            "getDungeonSkeleton": self.get_dungeon_skeleton,
        }
        self.actions.setdefault("default", UtilityModule.generate_response)

    def connectionMade(self):
        """
        Sending response that connection made and adding to connections list
        :return:
        """
        self.authorized_users[self.addr.port] = {
            'host': self.addr.host,
            'type': self.addr.type,
            'authorized': False,
            'main': {}
        }
        self.log_file.log_all(3, f"{self.addr.host}:{self.addr.port} Connected...")
        self.send_one(UtilityModule.generate_response(
            action="Connect to server",
            code=100
        ))

    def connectionLost(self, reason=ConnectionError):
        """
        Deleting connection from connections list if lost
        :param reason:
        :return:
        """
        if self.authorized_users:
            if self.addr.port in self.authorized_users:
                # pprint(self.authorized_users)
                print(f"DELETE CONNECTION WITH < {self.addr.host}:{self.addr.port} >")
                del self.authorized_users[self.addr.port]
                # pprint(self.authorized_users)
                self.cursor.disconnect()
                self.log_file.log_all(3, f"Connection lost with {self.addr.host}:{self.addr.port}")

    def send_private_message(self, action: str, json_data: Any):
        """
        Sending message to the another specified user from a specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        data = {
            'from': self.player.player_name,
            'to': json_data['data']['to'],
            'message': json_data['data']['message']
        }

        self.send_to_spec_user(data['from'], data['to'], UtilityModule.generate_response(action, 200, data))

    def send_chat_message(self, action: str, json_data: Any):
        """
        Sending message to the cat from a specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        data = {
            'from': json_data['data']['player_name'],
            'message': json_data['data']['message']
        }
        self.send_all(UtilityModule.generate_response(action, 200, data))

    def player_registration(self, action: str, json_data: Any):
        """
        Registration of specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        try:

            if self.cursor.check_player_name(json_data['data']['player_name']) == 1:
                self.send_one(UtilityModule.generate_response(action, 405))

            elif self.cursor.add_player(json_data['data']['player_name'],
                                        UtilityModule.encrypt_password(json_data['data']['player_password']),
                                        json_data['data']['class_id'],
                                        json_data['data']['race_id']
                                        ) == 1:

                self.send_one(UtilityModule.generate_response(action, 406))
                self.log_file.log_all(3, f"Player < {json_data['data']['player_name']} > successfully registered")

        except CustomExceptions.QueryExecuteError as query_exec_error:
            self.send_one(UtilityModule.generate_response(action, 400))
            self.log_file.log_all(2, query_exec_error)

    def player_authorization(self, action: str, json_data: Any):
        """
        Authorization of specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        try:
            if self.cursor.check_player_name(json_data['data']['player_name']) == 1:
                if self.cursor.check_player(
                        json_data['data']['player_name'],
                        UtilityModule.encrypt_password(json_data['data']['player_password'])
                ) == 1:
                    self.player = UserModule(player_data=self.cursor.get_player(json_data['data']['player_name']))

                    self.authorized_users[self.addr.port]['main'] ={
                        'player_name': self.player.player_name,
                        'base': self
                    }
                    self.authorized_users[self.addr.port]['authorized'] = True

                    self.send_one(UtilityModule.generate_response(action, 200, self.player.get_player_stats()))
                    self.log_file.log_all(3, f"Player < {json_data['data']['player_name']} > successfully authorized")
                else:
                    self.send_one(UtilityModule.generate_response(action, 407))
            else:
                # print("Hello")
                self.send_one(UtilityModule.generate_response(action, 407))
        except CustomExceptions.QueryExecuteError as query_exec_error:
            self.send_one(UtilityModule.generate_response(action, 400))
            self.log_file.log_all(2, query_exec_error)

    def get_dungeon_skeleton(self, action: str, json_data: Any):
        """
        Generate and send dungeon skeleton for the player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        try:
            if self.authorized_users[self.addr.port].get('authorized'):
                self.send_one(
                    UtilityModule.generate_response(
                        action=action,
                        code=201,
                        data={
                            "dungeonSkeleton": self.dungeon_generator.final_dungeon_skeleton(
                                player_data=self.player
                            )
                        }
                    )
                )
            else:
                self.send_one(UtilityModule.generate_response(action, 407))

        except Exception as exception:
            self.log_file.log_all(2, str(exception))
            self.send_one(UtilityModule.generate_response(action, 400))

    def lineReceived(self, line):
        """
        Receive line and parse it to json_data.
        Call method depending on action stored in json_data
        :param line:
        :return:
        """
        try:
            json_data = json.loads(line.decode())
            action = json_data['action']

            try:
                print(json_data)
                if action in self.actions:
                    self.actions.get(action)(action, json_data)
                else:
                    self.send_one(
                        response=self.actions.get("default")(action, 403)
                    )

            except Exception as exception:
                print("This: ", exception.with_traceback(exception.__traceback__))
                self.log_file.log_all(2, str(exception))
                self.send_one(UtilityModule.generate_response(action, 400))
                self.cursor.disconnect()

        except json.decoder.JSONDecodeError as json_decode_error:
            self.log_file.log_all(2, str(json_decode_error))
            self.send_one(UtilityModule.generate_response(None, 401))

    def send_all(self, message):
        """
        Sending message to al authorized users
        :param message: Json object to send for all authorized users
        :return:
        """
        for port in self.authorized_users:

            if self.authorized_users[port]['authorized']:

                protocol = self.authorized_users.__getitem__(port)['main']['base'].transport.protocol
                protocol.sendLine(message)

    def send_one(self, response):
        """
        Send response from server
        :param response:
        :return:
        """
        print("Send_one: ", response)
        self.sendLine(response)

    def send_to_spec_user(self, from_player, to_player,  message):
        """
        Send a message to specified user from user
        :param from_player: User from whom to send
        :param to_player: User whom to send
        :param message: Message to send
        :return:
        """
        for port in self.authorized_users:

            if self.authorized_users[port]['authorized']:

                if self.authorized_users.__getitem__(port)['main']['player_name'] == from_player or to_player:

                    protocol = self.authorized_users.__getitem__(port)['main']['base'].transport.protocol
                    protocol.sendLine(message)
