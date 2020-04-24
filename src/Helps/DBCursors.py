class Cursor:
    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.record = None

    def check_cursor(self):
        self.cursor.execute("select database();")
        self.record = self.cursor.fetchone()
        return self.record

    def cursor_close(self):
        self.cursor.close()

    def get_animals(self):
        self.cursor.execute(
            'select name, price, speed, capacity ' +
            'from Animals;'
        )
        self.record = self.cursor.fetchall()
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
