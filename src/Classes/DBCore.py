from .MySQLModule import MySQLModule
from .Logging import Log

class DBCore(MySQLModule):
    def __init__(self):
        super(DBCore, self).__init__()
        self.log = Log(self.__class__)
        self.record = None

    def database_info(self):
        self.log.log_all(3,"Connected to MariaDB version: " + self.database_connection.get_server_info())
        self.log.log_all(3,"Connected to Database: " + self.db_name)

    def get_animals(self):
        animals = self.query('select name, price, speed, capacity from Animals;')
        return animals

    def get_weapons(self):
        weapons = self.query('select name, price, damage_min, damage_max, weight from Weapons')

        return weapons

    def get_classes(self):
        self.cursor.execute(
            'select class_name ' +
            'from Classes;'
        )
        self.record = self.cursor.fetchall()
        return self.record

    def get_races(self):
        self.cursor.execute(
            'select name ' +
            'from Races;'
        )
        self.record = self.cursor.fetchall()
        return self.record

    def get_food(self):
        self.cursor.execute(
            'select name, price ' +
            'from Food;'
        )
        self.record = self.cursor.fetchall()
        return self.record

    def get_armor(self):
        armor = self.query( 'select name, armor_price, armor_weight from Armor')

        return armor
