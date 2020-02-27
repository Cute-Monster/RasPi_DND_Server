import os
import json
import mysql.connector as maria_db
from datetime import datetime


class Connection:
    def __init__(self):
        self.arch = os.system('arch')
        self.db_port = 3306
        self.config = self.get_config()
        # file.close()
        self.error_log_file = open("src/logs/errors.log", "w")
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
            self.cursor = self.database_connection.cursor()
        self.database_info()

    @staticmethod
    def get_config():
        with open(r"src/Classes/configs/config.json", "r") as file:
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
            self.error_log_file.writelines("{}: Connection error: {}".format(datetime.now(), str(e)))
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
        self.cursor = self.database_connection.cursor()
        self.cursor.execute("select database();")
        record = self.cursor.fetchone()
        print("connected to Database: ", record[0])

    def test_cursor(self):
        self.cursor.execute("SELECT name, speed FROM Animals;")
        animals = self.cursor.fetchall()
        print(dict(animals))

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
            self.error_log_file.writelines("{}: sshtunnel import Error: {}\n".format(datetime.now(), str(e)))
            return None

    def disconnect(self):
        if self.database_connection.is_connected():
            self.cursor.close()
            self.database_connection.close()
            print("Cursor closed\n"
                  "Database Connection closed")
        try:
            if (not self.raspberry) or (self.ssh_connection is not None):
                if self.ssh_connection.is_active:
                    self.ssh_connection.close()
                    print("SSH tunnel closed")
        except AttributeError as e:
            self.error_log_file.writelines("{}: Attribute error in Connection class disconnect method: {}"
                                           .format(datetime.now(), str(e)))
        finally:
            self.error_log_file.close()
