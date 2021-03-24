"""
MySqlModule.py: Module for connecting to the DataBase
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru"
__status__ = "Developing"


import os
from platform import platform
import json
from typing import Union

import mysql.connector as maria_db
from mysql.connector import CMySQLConnection, MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.cursor_cext import CMySQLCursor
from sshtunnel import SSHTunnelForwarder

from src.Logging.Logger import Log
from src.CustomExceptions import DBExceptions


class MySQLModule:
    """
    Class which describes behaviour of connection to the DataBase
    """

    def __init__(self):
        self._log: Log = Log(self.__class__)

        self._db_port: int = 3306

        # Getting computer WAN address
        self._computerAddress: str = self._get_ip_address()

        self._config: dict = self._get_config()
        if (platform().__contains__("armv7")) and (
            "178.132." not in self._computerAddress
        ):
            self._raspberry: bool = True
            self._ssh_connection: Union[None, SSHTunnelForwarder] = None
        else:
            self._raspberry: bool = False
            self._ssh_host: Union[str, int] = self._config["Connection"]["SSH"]["host"]
            self._ssh_port: Union[str, int] = self._config["Connection"]["SSH"]["port"]
            self._ssh_username: str = self._config["Connection"]["SSH"]["username"]
            self._ssh_password: str = self._config["Connection"]["SSH"]["password"]
            self._ssh_connection: SSHTunnelForwarder = self._ssh_connect()

            if self._ssh_connection is not None:
                self._db_port: Union[str, int] = self._ssh_connection.local_bind_port
                self._log.log_all(
                    3, "Local bind port: " + str(self._ssh_connection.local_bind_port)
                )

        self._db_host: Union[str, int] = self._config["Connection"]["DataBase"]["host"]
        self._db_username: str = self._config["Connection"]["DataBase"]["username"]
        self._db_password: str = self._config["Connection"]["DataBase"]["password"]
        self._db_name: str = self._config["Connection"]["DataBase"]["database_name"]

        self._database_connection: Union[
            CMySQLConnection, MySQLConnection, None
        ] = self._database_connect()
        self._cursor: Union[CMySQLCursor, MySQLCursor, None] = (
            self._database_connection.cursor(dictionary=True)
            if self._database_connection.is_connected()
            else None
        )

    @staticmethod
    def _get_ip_address() -> str:
        """
        Method to get ip address of the device on which script is being start
        :return:
        """

        from requests import get

        return get("https://api.ipify.org").text

    def _get_config(self) -> dict:
        """
        Method which gets config file based on ip address of  the device
        :return:
        """

        try:
            with open(
                "{}/{}.json".format(
                    os.path.abspath("src/Config"),
                    (
                        "home_connection_config"
                        if "178.132." in self._computerAddress
                        else "config"
                    ),
                ),
                "r",
            ) as file:
                config = json.load(file)
            return config
        except IOError as io_error:
            self._log.log_all(1, str(io_error))
            # print(io_error)

    def _database_connect(self) -> maria_db.connect:
        """
        Method to connect to the DataBase
        :return: database connection object
        """

        try:
            self._database_connection: Union[
                CMySQLConnection, MySQLConnection
            ] = maria_db.connect(
                host=self._db_host,
                database=self._db_name,
                user=self._db_username,
                password=self._db_password,
                port=self._db_port,
            )
            self._log.log_all(3, "DataBase connection made")
            return self._database_connection

        except maria_db.Error as e:
            self._log.log_all(1, f"Connection error: {str(e)}")
            self.disconnect()
            return None

    def _check_database_connection(self) -> None:
        """
        Method to check database connection
        :return:
        """

        if not self._database_connection.is_connected():
            self._database_connection.reconnect(10, 1)

    def _ssh_connect(self) -> Union[SSHTunnelForwarder, None]:
        """
        Method by which SSH tunnel is create
        :return: SSHTunnelForwarder if connection created or None
        """

        try:
            from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError

            try:
                ssh_connection: SSHTunnelForwarder = SSHTunnelForwarder(
                    (self._ssh_host, self._ssh_port),
                    ssh_username=self._ssh_username,
                    ssh_password=self._ssh_password,
                    remote_bind_address=(
                        self._config["Connection"]["SSH"]["remote_bind_address"][
                            "host"
                        ],
                        self._config["Connection"]["SSH"]["remote_bind_address"][
                            "port"
                        ],
                    ),
                )
                ssh_connection.start()
                self._log.log_all(3, "SSH Tunnel made")
                return ssh_connection
            except BaseSSHTunnelForwarderError as ssh_error:
                self._log.log_all(2, str(ssh_error))
                return None
        except ImportError as import_error:
            self._log.log_all(1, str(import_error))

    def disconnect(self) -> None:
        """
        Module which closes connection to the DataBase
        :return:
        """

        if self._database_connection.is_connected():
            self._cursor.close()
            self._database_connection.close()
            self._log.log_all(3, "Database Connection closed")
        try:
            if (not self._raspberry) or self._ssh_connection:
                if self._ssh_connection.is_active:
                    self._ssh_connection.close()
                    self._log.log_all(3, "SSH tunnel closed")
        except AttributeError as e:
            self._log.log_all(1, str(e))

    def select_query(self, query: str) -> list:
        """
        Module which executes SELECT query on the DataBase
        :param query: query to execute
        :return:
        """

        try:
            self._check_database_connection()
            self._cursor.execute(query)
            return self._cursor.fetchall()
        except maria_db.Error as error:
            self._log.log_all(1, str(error))
            raise DBExceptions.QueryExecuteError("Error to execute query:", error)

    def insert_query(self, query: str) -> int:
        """
        Module which executes INSERT query on the DataBase
        :param query: query to execute
        :return:
        """

        try:
            self._check_database_connection()
            self._cursor.execute(query)
            self._database_connection.commit()
            return 1
        except maria_db.Error as error:
            self._log.log_all(1, str(error))
            raise DBExceptions.QueryExecuteError("Error to execute query:", error)
