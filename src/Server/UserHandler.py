"""
UserHandler.py: Main module of server/Heart of the server
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

import json
from abc import ABC
from typing import Any
from twisted.protocols.basic import LineReceiver
import twisted.internet.error as twisted_error

from src.Logging.Logger import Log
from src.Modules import UtilityModule
from src.Modules.UserModule import UserModule
from src.Modules.DungeonSkeleton import DungeonSkeleton
from src.CustomExceptions import ChatExceptions, DBExceptions
from src.DB.DBCore import DBCore

from pprint import pprint


class UserHandler(LineReceiver, ABC):
    """
    Heart of the server
    """
    def __init__(self,
                 cursor: DBCore,
                 users: dict,
                 addr):
        self.cursor = cursor
        self.dungeon_generator = DungeonSkeleton(
            cursor=self.cursor
        )
        self.connected_users = users
        self.addr = addr
        self.user_key = f"{self.addr.host}:{self.addr.port}"
        self.player = UserModule
        self.log_file = Log(
            module=self.__class__
        )
        self.actions = {
            "default": UtilityModule.generate_response,
            "playerRegistration": self.player_registration,
            "playerAuthorization": self.player_authorization,
            "sendChatMessage": self.send_chat_message,
            "sendPrivateMessage": self.send_private_message,
            "getDungeonSkeleton": self.get_dungeon_skeleton,
        }
        # pprint(self.actions)

    def connectionMade(self):
        """
        Sending response that connection made and adding to connections list
        :return:
        """

        self.connected_users[self.user_key] = {
            'host': self.addr.host,
            'type': self.addr.type,
            'authorized': False,
            'main': {}
        }
        self.log_file.log_all(
            priority=3,
            string=f"{self.addr.host}:{self.addr.port} Connected to server"
        )
        self.send_one(
            response=UtilityModule.generate_response(
                action="connectToServer",
                code=100
            )
        )

    def connectionLost(self,
                       reason=twisted_error):
        """
        Deleting connection from connections list if lost
        :param reason:
        :return:
        """

        # print(reason.getErrorMessage())
        if self.connected_users:
            if self.user_key in self.connected_users:
                print(f"DELETE CONNECTION WITH < {self.addr.host}:{self.addr.port} >")
                del self.connected_users[self.user_key]
                self.log_file.log_all(
                    priority=3,
                    string=f"Connection lost with {self.addr.host}:{self.addr.port} "
                           f"-> Reason: {reason.getErrorMessage()}"
                )

    def send_private_message(self,
                             action: str,
                             json_data: Any) -> None:
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
        try:
            self.send_to_spec_user(
                to_player=json_data['data']['to'],
                message=UtilityModule.generate_response(
                    action=action,
                    code=200,
                    data=data
                )
            )
        except ChatExceptions.ChatException as chat_exception:
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=409
                )
            )

    def send_chat_message(self,
                          action: str,
                          json_data: Any) -> None:
        """
        Sending message to the cat from a specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        data = {
            'from': self.player.player_name,
            'message': json_data['data']['message']
        }
        self.send_all(
            message=UtilityModule.generate_response(
                action=action,
                code=200,
                data=data
            )
        )

    def player_registration(self,
                            action: str,
                            json_data: Any) -> None:
        """
        Registration of specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        try:

            if self.cursor.check_player_name(
                    name=json_data['data']['player_name']
            ) == 1:
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=405
                    )
                )

            elif self.cursor.add_player(
                    name=json_data['data']['player_name'],
                    password=UtilityModule.encrypt_password(
                        player_password=json_data['data']['player_password']
                    ),
                    class_id=json_data['data']['class_id'],
                    race_id=json_data['data']['race_id']
            ) == 1:

                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=406
                    )
                )
                self.log_file.log_all(
                    priority=3,
                    string=f"Player < {json_data['data']['player_name']} > successfully registered"
                )

        except DBExceptions.QueryExecuteError as query_exec_error:
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=400
                )
            )
            self.log_file.log_all(
                priority=2,
                string=query_exec_error
            )

    def player_authorization(self,
                             action: str,
                             json_data: Any) -> None:
        """
        Authorization of specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        try:
            if self.cursor.check_player_name(
                    name=json_data['data']['player_name']
            ) == 1:
                if self.cursor.check_player(
                        name=json_data['data']['player_name'],
                        password=UtilityModule.encrypt_password(
                            player_password=json_data['data']['player_password']
                        )
                ) == 1:
                    self.player = UserModule(
                        player_data=self.cursor.get_player(
                            player_name=json_data['data']['player_name']
                        )
                    )

                    self.connected_users[self.user_key]['main'] = {
                        'player_name': self.player.player_name,
                        'base': self
                    }
                    self.connected_users[self.user_key]['authorized'] = True

                    self.send_one(
                        response=UtilityModule.generate_response(
                            action=action,
                            code=407,
                            data=self.player.get_player()
                        )
                    )
                    self.log_file.log_all(
                        priority=3,
                        string=f"Player < {json_data['data']['player_name']} > successfully authorized"
                    )
                else:
                    self.send_one(
                        response=UtilityModule.generate_response(
                            action=action,
                            code=410
                        )
                    )
            else:
                # print("Hello")
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=410
                    )
                )
        except DBExceptions.QueryExecuteError as query_exec_error:
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=400
                )
            )
            self.log_file.log_all(
                priority=2,
                string=query_exec_error
            )

    def get_dungeon_skeleton(self,
                             action: str,
                             json_data: Any) -> None:
        """
        Generate and send dungeon skeleton for the player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """
        try:
            if self.connected_users[self.user_key].get('authorized'):
                self.send_one(
                    response=UtilityModule.generate_response(
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
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=408
                    )
                )

        except Exception as exception:
            self.log_file.log_all(
                priority=2,
                string=exception
            )
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=400
                )
            )

    def lineReceived(self,
                     line):
        """
        Receive line and parse it to json_data.
        Call method depending on action stored in json_data
        :param line:
        :return:
        """
        try:
            json_data = json.loads(line.decode("utf8"))
            action = json_data['action']

            try:
                print(f"Received line: {json_data}")
                if action in self.actions:
                    self.actions.get(action)(action, json_data)
                else:
                    self.send_one(
                        response=self.actions.get("default")(action, 403)
                    )

            except Exception as exception:
                print(f"Exception in lineReceived: {exception}")
                self.log_file.log_all(
                    priority=2,
                    string=exception
                )
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=400
                    )
                )
                # self.cursor.disconnect()

        except json.decoder.JSONDecodeError as json_decode_error:
            self.log_file.log_all(
                priority=2,
                string=json_decode_error
            )
            self.send_one(
                response=UtilityModule.generate_response(
                    action=None,
                    code=401
                )
            )

    def send_all(self,
                 message: bytes) -> None:
        """
        Sending message to al authorized users
        :param message: Json object to send for all authorized users
        :return:
        """
        pprint(json.loads(message))
        for user_key in self.connected_users:

            if self.connected_users[user_key]['authorized']:

                protocol = self.connected_users[user_key]['main']['base'].transport.protocol
                protocol.sendLine(
                    line=message
                )

    def send_one(self,
                 response: bytes) -> None:
        """
        Send response from server
        :param response:
        :return:
        """

        pprint(json.loads(response))
        self.sendLine(
            line=response
        )

    def send_to_spec_user(self,
                          to_player: str,
                          message: bytes) -> None:
        """
        Send a message to specified user from user
        :param to_player: User whom to send
        :param message: Message to send
        :return:
        """
        pprint(json.loads(message))
        user_to_logged = False
        user_to_key = ""
        if self.cursor.check_player_name(
                name=to_player
        ) == 1:
            for user_key in self.connected_users:

                if self.connected_users[user_key]['authorized']:

                    if self.connected_users[user_key]['main']['player_name'] == to_player:
                        user_to_logged = True
                        user_to_key = user_key
                        break
        else:
            raise ChatExceptions.ChatException("player not registered")
        if user_to_logged:
            self.sendLine(
                line=message
            )
            protocol = self.connected_users[user_to_key]['main']['base'].transport.protocol
            protocol.sendLine(
                line=message
            )
        else:
            raise ChatExceptions.ChatException("player not logged")
