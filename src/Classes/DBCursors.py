from .Connection import Connection


class Cursor(Connection):
    def __init__(self):
        super(Cursor, self).__init__()
        self.cursor = self.database_connection.cursor()
        self.record = None

    def database_info(self):
        print("connected to MariaDB version: ", self.database_connection.get_server_info())
        print("connected to Database: ", self.check_cursor())

    def check_cursor(self):
        self.cursor.execute("select database();")
        self.record = self.cursor.fetchone()
        return self.record

    def cursor_close(self):
        self.cursor.close()

    def get_animals(self):
        self.record = self.cursor.execute(
            'select name, price, speed, capacity ' +
            'from Animals;'
        ).fetchall()
        return self.record

    def get_weapons(self):
        self.cursor.execute(
            'select name, price, damage_min, damage_max, weight ' +
            'from Weapons;'
        )
        self.record = self.cursor.fetchall()
        return self.record

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
        self.cursor.execute(
            'select CodeDungeon.Armor.name, CodeDungeon.Armor.armor_price, CodeDungeon.Armor.armor_weight ' +
            'from CodeDungeon.Armor;'
        )
        self.record = self.cursor.fetchall()
        return self.record
