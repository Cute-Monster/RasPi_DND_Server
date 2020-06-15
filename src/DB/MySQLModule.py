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
import mysql.connector as maria_db
from src.Logging.Logger import Log
from src.CustomExceptions import DBExceptions


class MySQLModule:
    """
    Class which describes behaviour of connection to the DataBase
    """
    def __init__(self):
        self.log = Log(self.__class__)

        self.db_port = 3306

        # Getting computer WAN address
        self.computerAddress = self.get_ip_address()

        self.config = self.get_config()
        if ("armv7" in platform()) and ("178.132." not in self.computerAddress):
            self.raspberry = True
            self.ssh_connection = None
        else:
            self.raspberry = False
            self.ssh_host = self.config['Connection']['SSH']['host']
            self.ssh_port = self.config['Connection']['SSH']['port']
            self.ssh_username = self.config['Connection']['SSH']['username']
            self.ssh_password = self.config['Connection']['SSH']['password']
            self.ssh_connection = self.ssh_connect()

            if self.ssh_connection is not None:
                self.db_port = self.ssh_connection.local_bind_port
                self.log.log_all(3, "Local bind port: " + str(self.ssh_connection.local_bind_port))

        self.db_host = self.config['Connection']['DataBase']['host']
        self.db_username = self.config['Connection']['DataBase']['username']
        self.db_password = self.config['Connection']['DataBase']['password']
        self.db_name = self.config['Connection']['DataBase']['database_name']

        self.database_connection = self.database_connect()
        self.cursor = (
            self.database_connection.cursor(dictionary=True) if self.database_connection.is_connected() else None
        )

    @staticmethod
    def get_ip_address() -> str:
        """
        Method to get ip address of the device on which script is being start
        :return:
        """

        from requests import get
        return get('https://api.ipify.org').text

    def get_config(self) -> dict:
        """
        Method which gets config file based on ip address of  the device
        :return:
        """

        try:
            with open(
                    "{}/{}.json".format(
                        os.path.abspath('src/Config'),
                        ("home_connection_config" if "178.132." in self.computerAddress else "config")),
                    "r") as file:
                config = json.load(file)
            return config
        except IOError as io_error:
            self.log.log_all(1, str(io_error))
            # print(io_error)

    def database_connect(self) -> maria_db.connect:
        """
        Method to connect to the DataBase
        :return: database connection object
        """

        try:
            self.database_connection = maria_db.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_username,
                password=self.db_password,
                port=self.db_port
            )
            self.log.log_all(3, "DataBase connection made")
            return self.database_connection

        except maria_db.Error as e:
            self.log.log_all(1, f"Connection error: {str(e)}")
            self.disconnect()
            return None

    def check_database_connection(self):
        """
        Method to check database connection
        :return:
        """

        if not self.database_connection.is_connected():
            self.database_connection.reconnect(10, 1)

    def ssh_connect(self):
        """
        Method by which SSH tunnel is create
        :return: SSHTunnelForwarder if connection created or None
        """

        try:
            from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError
            try:
                ssh_connection = SSHTunnelForwarder(
                    (self.ssh_host, self.ssh_port),
                    ssh_username=self.ssh_username,
                    ssh_password=self.ssh_password,
                    remote_bind_address=(
                        self.config['Connection']['SSH']['remote_bind_address']['host'],
                        self.config['Connection']['SSH']['remote_bind_address']['port']
                    )
                )
                ssh_connection.start()
                self.log.log_all(3, "SSH Tunnel made")
                return ssh_connection
            except BaseSSHTunnelForwarderError as ssh_error:
                self.log.log_all(2, str(ssh_error))
                return None
        except ImportError as import_error:
            self.log.log_all(1, str(import_error))

    def disconnect(self):
        """
        Module which closes connection to the DataBase
        :return:
        """

        if self.database_connection.is_connected():
            self.cursor.close()
            self.database_connection.close()
            self.log.log_all(3, "Database Connection closed")
        try:
            if (not self.raspberry) or self.ssh_connection:
                if self.ssh_connection.is_active:
                    self.ssh_connection.close()
                    self.log.log_all(3, "SSH tunnel closed")
        except AttributeError as e:
            self.log.log_all(1, str(e))

    def select_query(self, query):
        """
        Module which executes SELECT query on the DataBase
        :param query: query to execute
        :return:
        """

        try:
            self.check_database_connection()
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except maria_db.Error as error:
            self.log.log_all(1, str(error))
            # raise custom_error_exception("Error to execute query", error)
            raise DBExceptions.QueryExecuteError("Error to execute query:", error)

    def insert_query(self, query) -> int:
        """
        Module which executes INSERT query on the DataBase
        :param query: query to execute
        :return:
        """

        try:
            self.check_database_connection()
            self.cursor.execute(query)
            self.database_connection.commit()
            return 1
        except maria_db.Error as error:
            self.log.log_all(1, str(error))
            # raise custom_error_exception("Error to execute query", error)
            raise DBExceptions.QueryExecuteError("Error to execute query:", error)
