"""
UserHandler.py: Main module of server/Heart of the server
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.2.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

import json
from abc import ABC
from typing import Any
from twisted.protocols.basic import LineReceiver
import twisted.internet.error as twisted_error
from datetime import datetime

from src.Logging.Logger import Log
from src.Modules import UtilityModule, LootModule, BattleModule
from src.Modules.UserModule import UserModule
from src.Modules.DungeonSkeleton import DungeonSkeleton
from src.CustomExceptions import ChatExceptions, DBExceptions
from src.DB.DBCore import DBCore


class UserHandler(LineReceiver, ABC):
    """
    Heart of the server
    """

    def __init__(self,
                 cursor: DBCore,
                 users: dict,
                 addr
                 ):
        self.cursor = cursor
        self.dungeon_generator = DungeonSkeleton(
            cursor=self.cursor
        )
        self.connected_users = users
        self.addr = addr
        self.user_key = f"{self.addr.host}:{self.addr.port}"
        self.player = UserModule
        self.log_file = Log(
            class_name=self.__class__
        )
        self.actions = {
            "default": UtilityModule.generate_response,
            "playerRegistration": self.player_registration,
            "playerAuthorization": self.player_authorization,
            "getDungeonSkeleton": self.get_dungeon_skeleton,
            "regenerateDungeonSkeleton": self.regen_dungeon_skeleton,
            "startBattle": self.start_battle,
            "getLoot": self.generate_loot,
            "sendChatMessage": self.send_chat_message,
            "sendPrivateMessage": self.send_private_message
        }

    def log_to_debug(self,
                     line: str
                     ) -> None:
        """
        Log to the debug file
        :param line: Line to log
        """

        with open("Logs/debug.log", "a") as f:
            f.writelines(f"{self.user_key} | {datetime.now()} | {line}\n")

    @staticmethod
    def log_account_info(username: str,
                         password: str
                         ) -> None:
        """
        Log players Username and Password
        :param username: Players username
        :param password: Players password
        :return:
        """

        with open("Logs/user_registry.log", "a") as file:
            file.writelines(
                f"Registered: {datetime.now()} | Username: {username} | Password: {password}\n"
            )

    def connectionMade(self):
        """
        Sending response that connection made and adding to connections list
        :return:
        """

        self.connected_users[self.user_key] = {
            "host": self.addr.host,
            "type": self.addr.type,
            "authorized": False,
            "main": {
                "player_name": None,
                "base": None,
                "dungeon": None
            },
        }
        self.log_to_debug(
                line=f"Connected to server..."
        )
        self.log_file.log_all(
            priority=3,
            string=f"{self.addr.host}:{self.addr.port} Connected to server..."
        )
        self.send_one(
            response=UtilityModule.generate_response(
                action="connectToServer",
                code=100
            )
        )

    def lineReceived(self,
                     line: bytes
                     ):
        """
        Receive line and parse it to json_data.
        Call method depending on action stored in json_data
        :param line:
        :return:
        """
        # print(f"Before_Loads -> {line}")
        try:
            json_data = json.loads(line.decode("utf8"))
            action = json_data['action']

            try:
                self.log_to_debug(
                    line=f"Received line: {json_data}"
                )
                if action in self.actions:
                    self.actions.get(action)(action, json_data)
                else:
                    self.send_one(
                        response=self.actions.get("default")(action, 403)
                    )

            except Exception as exception:
                print("Exception -> ", exception)
                self.log_file.log_all(
                    priority=2,
                    string=str(exception)
                )
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=400
                    )
                )

        except json.decoder.JSONDecodeError as json_decode_error:
            self.log_file.log_all(
                priority=2,
                string=str(json_decode_error)
            )
            self.send_one(
                response=UtilityModule.generate_response(
                    action=None,
                    code=401
                )
            )

    def connectionLost(self,
                       reason=twisted_error
                       ):
        """
        Deleting connection from connections list if lost
        :param reason:
        :return:
        """

        if self.connected_users and self.user_key in self.connected_users:
            self.log_to_debug(
                line=f"DELETE CONNECTION.. -> Reason: {reason.getErrorMessage()}"
            )
            del self.connected_users[self.user_key]
            self.log_file.log_all(
                priority=3,
                string=f"Connection lost with {self.addr.host}:{self.addr.port} "
                       f"-> Reason: {reason.getErrorMessage()}"
            )

    def player_registration(self,
                            action: str,
                            json_data: Any
                            ) -> None:
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
                        code=202
                    )
                )

                self.log_account_info(
                    username=json_data['data']['player_name'],
                    password=json_data['data']['player_password']
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
                string=str(query_exec_error)
            )

    def player_authorization(self,
                             action: str,
                             json_data: Any
                             ) -> None:
        """
        Authorization of specified player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """

        def check_for_user_not_in_system(player_name: str) -> bool:
            """
            Checking if user with given username already logged
            :param player_name:
            :return:
            """

            for uid, user in self.connected_users.items():
                if user['authorized'] and user['main']['player_name'] == player_name:
                    return False
            return True

        try:
            if self.cursor.check_player_name(
                    name=json_data['data']['player_name']
            ) == 1:
                if check_for_user_not_in_system(json_data['data']['player_name']) \
                        or len(self.connected_users) == 1:
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

                        self.connected_users[self.user_key]['main']['player_name'] = self.player.player_name
                        self.connected_users[self.user_key]['main']['base'] = self
                        self.connected_users[self.user_key]['authorized'] = True

                        self.send_one(
                            response=UtilityModule.generate_response(
                                action=action,
                                code=203,
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
                                code=408
                            )
                        )
                else:
                    self.send_one(
                        response=UtilityModule.generate_response(
                            action=action,
                            code=409
                        )
                    )
            else:
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=408
                    )
                )
        except DBExceptions.QueryExecuteError as query_exec_error:
            # print("Player_Auth_Err -> ", query_exec_error)
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=400
                )
            )
            self.log_file.log_all(
                priority=2,
                string=str(query_exec_error)
            )

    def get_dungeon_skeleton(self,
                             action: str,
                             json_data: Any
                             ) -> None:
        """
        Generate and send dungeon skeleton for the player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """

        try:
            if self.connected_users[self.user_key].get('authorized'):
                if not self.connected_users[self.user_key]['main']['dungeon']: 
                    skeleton = self.dungeon_generator.final_dungeon_skeleton(
                        player_data=self.player
                    )
                    self.connected_users[self.user_key]['main']['dungeon'] = {
                        'skeleton': skeleton,
                        'passed': False
                    }
                    self.send_one(
                        response=UtilityModule.generate_response(
                            action=action,
                            code=201,
                            data={
                                "dungeonSkeleton": skeleton
                            }
                        )
                    )
                else:
                    self.send_one(
                            response=UtilityModule.generate_response(
                                action=action,
                                code=411
                                )
                            )
            else:
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=406
                    )
                )

        except Exception as exception:
            self.log_file.log_all(
                priority=2,
                string=str(exception)
            )
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=400
                )
            )

    def regen_dungeon_skeleton(self,
                               action: str,
                               json_data: Any
                               ) -> None:
        """
        Generate and send dungeon skeleton for the player
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """

        try:
            if self.connected_users[self.user_key].get('authorized'):
                if self.connected_users[self.user_key]['main']['dungeon']:
                    self.connected_users[self.user_key]['main']['dungeon'] = None
                    self.get_dungeon_skeleton(
                        action=action,
                        json_data=json_data
                    )
                else:
                    self.send_one(
                            response=UtilityModule.generate_response(
                                action=action,
                                code=410
                                )
                            )
            else:
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=406
                    )
                )

        except Exception as exception:
            self.log_file.log_all(
                priority=2,
                string=str(exception)
            )
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=400
                )
            )

    def start_battle(self,
                     action: str,
                     json_data: Any
                     ) -> None:
        """
        Method for invoking battle between a player and given enemy
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """

        battle = BattleModule.BattleModule(
            player=self.player,
            battle_data=json_data['data']
        ).battle_result()
        self.send_one(
            response=UtilityModule.generate_response(
                action=action,
                code=205,
                data=battle
            )
        )

    def generate_loot(self,
                      action: str,
                      json_data: Any
                      ) -> None:
        """
        Method to generate loot after passing the dungeon
        :param action: String used to generate response
        :param json_data: Received data from the client
        :return:
        """

        if self.connected_users[self.user_key]['authorized']:
            if self.connected_users[self.user_key]['main']['dungeon']:  # fixme check if dungeon complete
                available_loot = self.cursor.get_loot()
                self.connected_users[self.user_key]['main']['dungeon']['passed'] = True
                result = LootModule.LootModule(
                    dungeon=self.connected_users[self.user_key]['main']['dungeon']['skeleton'],
                    player=self.player,
                    loot=available_loot).get_loot()
                result['level'] = self.player.level_up(
                    received_experience=result['level']
                )
                self.connected_users[self.user_key]['main']['dungeon'] = None
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=204,
                        data=result
                    )
                )
                del result
                del available_loot
            else:
                self.send_one(
                    response=UtilityModule.generate_response(
                        action=action,
                        code=410
                    )
                )
        else:
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=406
                )
            )

    def send_private_message(self,
                             action: str,
                             json_data: Any
                             ) -> None:
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
        except ChatExceptions.ChatException:
            self.send_one(
                response=UtilityModule.generate_response(
                    action=action,
                    code=407
                )
            )

    def send_chat_message(self,
                          action: str,
                          json_data: Any
                          ) -> None:
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

    def send_all(self,
                 message: bytes
                 ) -> None:
        """
        Sending message to al authorized users
        :param message: Json object to send for all authorized users
        :return:
        """

        self.log_to_debug(
                line=f"Send_All: {message}"
                )
        for user_key in self.connected_users:

            if self.connected_users[user_key]['authorized']:
                protocol = self.connected_users[user_key]['main']['base'].transport.protocol
                protocol.sendLine(
                    line=message
                )

    def send_one(self,
                 response: bytes
                 ) -> None:
        """
        Send response from server
        :param response:
        :return:
        """

        self.log_to_debug(
            line=f"Send_One: {response} "
            )
        self.sendLine(
            line=response
        )

    def send_to_spec_user(self,
                          to_player: str,
                          message: bytes
                          ) -> None:
        """
        Send a message to specified user from user
        :param to_player: User whom to send
        :param message: Message to send
        :return:
        """

        self.log_to_debug(
                line=f"Send_To_Spec: {message}"
                )
        user_to_logged = False
        user_to_key = ""
        if self.cursor.check_player_name(
                name=to_player
        ) == 1:
            for user_key in self.connected_users:

                if self.connected_users[user_key]['authorized'] \
                        and self.connected_users[user_key]['main']['player_name'] == to_player:
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
