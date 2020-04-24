import os
import json
import mysql.connector as maria_db
from datetime import datetime
from src.Helps.DBCursors import Cursor as DBCursor


class Connection:
    def __init__(self):
        self.arch = os.system('arch')
        self.db_port = 3306
        self.error_log_file = open("{}/errors.log".format(os.path.abspath('logs')), "a")
        # Getting computer inet address
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
                print("Local bind port: ", self.ssh_connection.local_bind_port)
        self.db_host = self.config['Connection']['DataBase']['host']
        self.db_username = self.config['Connection']['DataBase']['username']
        self.db_password = self.config['Connection']['DataBase']['password']
        self.db_name = self.config['Connection']['DataBase']['database_name']

        self.database_connection = self.database_connect()
        if self.check_database_connection():
            self.cursor = DBCursor(self.database_connection)
        self.database_info()

    def get_ip_address(self):
        # import socket
        # import fcntl
        # import struct
        #
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # try:
        #     return socket.inet_ntoa(fcntl.ioctl(
        #         s.fileno(),
        #         0x8915,  # SIOCGIFADDR
        #         struct.pack('256s', bytes("wlan0"[:15], 'utf-8'))
        #     )[20:24])
        # except Exception as exception:
        #     self.error_log_file.writelines("{}: {}".format(datetime.now(), exception))
        #     return socket.inet_ntoa(fcntl.ioctl(
        #         s.fileno(),
        #         0x8915,  # SIOCGIFADDR
        #         struct.pack('256s', bytes("eth0"[:15], 'utf-8'))
        #     )[20:24])
        from requests import get
        # ip = get('https://api.ipify.org').text
        return get('https://api.ipify.org').text

    def get_config(self):
        with open(
                "{}/{}.json".format(
                    os.path.abspath('Classes/configs'),
                    'home_connection_config' if '178.132.' in self.computerAddress else 'config'),
                "r") as file:
            config = json.load(file)
        print("GET")
        return config

    def database_connect(self):
        connection = None
        try:
            connection = maria_db.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_username,
                password=self.db_password,
                port=self.db_port
            )
        except maria_db.Error as e:
            self.error_log_file.writelines("{}: Connection error: {}\n".format(datetime.now(), str(e)))
            self.disconnect()
            return None
        finally:
            return connection

    def check_database_connection(self):
        if self.database_connection.is_connected():
            return True
        else:
            return False

    def database_info(self):
        print("connected to MariaDB version: ", self.database_connection.get_server_info())
        # self.cursor = self.database_connection.cursor()
        # self.cursor.execute("select database();")
        # record = self.cursor.fetchone()
        print("connected to Database: ", self.cursor.check_cursor())

    def test_cursor(self):
        animals = self.cursor.get_animals()
        print(animals)

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
            self.error_log_file.writelines("{}: {}\n".format(datetime.now(), str(e)))
            return None

    def disconnect(self):
        if self.database_connection.is_connected():
            self.cursor.cursor_close()
            self.database_connection.close()
            print("Cursor closed\n"
                  "Database Connection closed")
        try:
            if (not self.raspberry) or (self.ssh_connection is not None):
                if self.ssh_connection.is_active:
                    self.ssh_connection.close()
                    print("SSH tunnel closed")
        except AttributeError as e:
            self.error_log_file.writelines("{}: {}\n" .format(datetime.now(), str(e)))
        finally:
            self.error_log_file.close()
