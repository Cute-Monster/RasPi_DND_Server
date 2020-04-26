import os
import json
import mysql.connector as maria_db
from .Logging import Log

class MySQLModule:
    def __init__(self):
        self.log = Log(self.__class__)

        self.arch = os.system('arch')
        self.db_port = 3306

        # Getting computer WAN address
        self.computerAddress = self.get_ip_address()
        self.config = self.get_config()
        if self.arch is "armv71":
            self.raspberry = True
        else:
            self.raspberry = False
            self.ssh_host = self.config['Connection']['SSH']['host']
            self.ssh_port = self.config['Connection']['SSH']['port']
            self.ssh_username = self.config['Connection']['SSH']['username']
            self.ssh_password = self.config['Connection']['SSH']['password']
            self.ssh_connection = self.ssh_connect()

            if self.ssh_connection is not None:
                self.db_port = self.ssh_connection.local_bind_port
                self.log.log_all(3, "Local bind port: " + self.ssh_connection.local_bind_port)

        self.db_host = self.config['Connection']['DataBase']['host']
        self.db_username = self.config['Connection']['DataBase']['username']
        self.db_password = self.config['Connection']['DataBase']['password']
        self.db_name = self.config['Connection']['DataBase']['database_name']

        self.database_connection, self.cursor = None, None
        self.database_connect()

    @staticmethod
    def get_ip_address():
        from requests import get
        return get('https://api.ipify.org').text

    def get_config(self):
        with open(
                "{}/{}.json".format(
                    os.path.abspath('Classes/configs'),
                    'home_connection_config' if '178.132.' in self.computerAddress else 'config'),
                "r") as file:
            config = json.load(file)
        return config

    def database_connect(self):
        try:
            self.database_connection = maria_db.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_username,
                password=self.db_password,
                port=self.db_port
            )

            if self.database_connection.is_connected():
                self.cursor = self.database_connection.cursor()
        except maria_db.Error as e:
            self.log.log_all(1, "Connection error: " + str(e))
            self.disconnect()

    def check_database_connection(self):
        if not self.database_connection.is_connected():
            self.database_connection.reconnect(10, 1)

    def ssh_connect(self):
        try:
            from sshtunnel import SSHTunnelForwarder
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
            return ssh_connection
        except ImportError as e:
            self.log.log_all(1, str(e))
            return None

    def disconnect(self) -> None:
        if self.database_connection.is_connected():
            self.database_connection.close()
            self.log.log_all(3, "Database Connection closed")
        try:
            if (not self.raspberry) or (self.ssh_connection is not None):
                if self.ssh_connection.is_active:
                    self.ssh_connection.close()
                    self.log.log_all(3, "SSH tunnel closed")
        except AttributeError as e:
            self.log.log_all(1, str(e))
        finally:
            self.log.log_close()

    def query(self, query):
        try:
            self.check_database_connection()
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except maria_db.Error as error:
            self.log.log_all(1, str(error))
            return None