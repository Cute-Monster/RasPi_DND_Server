"""
DBCore.py: Module which contains methods to get useful data from DataBase
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghosatshow@yandex.ru "
__status__ = "Developing"

from .MySQLModule import MySQLModule
from src.Logging.Logger import Log

__all__ = ["DBCore"]


class DBCore(MySQLModule):
    """
    Class which contains methods to get useful data from DataBase
    """

    def __init__(self):
        super(DBCore, self).__init__()
        self.log = Log(self.__class__)

    def database_info(self):
        """
        Get information about DataBase version,Name and log this to file
        :return:
        """

        self.log.log_all(3, "Connected to MariaDB version: " + self.database_connection.get_server_info())
        self.log.log_all(3, "Connected to Database: " + self.db_name)

    def get_animals(self):
        """
        Getting animals from DataBase
        :return:
        """

        animals = self.select_query("""
        SELECT name, price, speed, capacity FROM Animals;
        """)
        return animals

    def get_weapons(self):
        """
        Getting weapons from DataBase
        :return:
        """

        weapons = self.select_query("""
        SELECT name, price, damage_min, damage_max, weight FROM Weapons
        """)

        return weapons

    def get_classes(self):
        """
        Getting classes from DataBase
        :return:
        """

        classes = self.select_query("""
        SELECT class_name FROM Classes;
        """)

        return classes

    def get_races(self):
        """
        Getting races from DataBase
        :return:
        """

        races = self.select_query("""
        SELECT name FROM Races;
        """)

        return races

    def get_food(self):
        """
        Getting available food from DataBase
        :return:
        """

        food = self.select_query("""
        SELECT name, price FROM Food;
        """)

        return food

    def get_armor(self):
        """
        Getting available armor from DataBase
        :return:
        """

        armor = self.select_query("""
        SELECT name, armor_price, armor_weight FROM Armor
        """)

        return armor

    def check_player(self, name, password) -> int:
        """
        Checking player for existing in DataBase
        :param name: Player name
        :param password: Player password
        :return:
        """

        exists = self.select_query(f"""
            SELECT EXISTS(
                SELECT player_name from Players WHERE player_name = '{name}' AND player_password = '{password}'
            ) AS `exists`;
        """)

        return exists[0]['exists']

    def check_player_name(self, name) -> int:
        """
        Checking player name for existing in DataBase
        :param name: Player name
        :return:
        """

        exists = self.select_query(f"""
            SELECT EXISTS(
                SELECT player_name from Players WHERE player_name = '{name}'
            ) AS `exists`;
        """)

        return exists[0]['exists']

    def add_player(self, name, password, class_id, race_id):
        """
        Adding player to the DataBase
        :param name: Player name
        :param password: Player password
        :param class_id: Player class id
        :param race_id: Player race id
        :return:
        """

        return self.insert_query(f"""
            INSERT INTO Players (player_name, player_password, lvl, experience, class_id, race_id) 
            VALUES('{name}', '{password}', 1, 0, {class_id}, {race_id})
        """)

    def get_player_main_data(self, name):
        """
        Getting main data about a player from DataBase
        :param name: Player Name
        :return:
        """

        return self.select_query(f"""SELECT
            `p`.`player_id`,
            `p`.`player_name`,
            `p`.`lvl`,
            `p`.`experience`,
            `p`.`class_id`,
            `c`.`class_name`,
            `p`.`race_id`,
            `r`.`name` AS `race`,
            `s`.*
        FROM
            Players AS p
            LEFT JOIN Races AS r ON r.race_id = p.race_id
            LEFT JOIN Classes AS c ON c.class_id = p.class_id
            LEFT JOIN Stats AS s ON s.hero_id = p.player_id 
        WHERE
            player_name = '{name}'
        """)

    def get_player_food(self, player_id):
        """
        Getting players food from DataBase
        :param player_id: Player id
        :return:
        """

        return self.select_query(f"""
            SELECT
                `fe`.`food_id`,
                `f`.`name` AS `food_name`,
                `f`.`price` AS `food_price`
            FROM
                `Food_Equipment` AS `fe`
                INNER JOIN `Food` AS `f` ON `f`.`food_id` = `fe`.`food_id`
            WHERE
                `fe`.`equipment_id` = '{player_id}'
        """)

    def get_player_armor(self, player_id):
        """
        Getting players armor from DataBase
        :param player_id: Player id
        :return:
        """

        return self.select_query(f"""
            SELECT
                `ae`.`armor_id`,
                `a`.`name` AS `armor_name`,
                `a`.`armor_weight`,
                `a`.`armor_price` 
            FROM
                `Armor_Equipment` AS `ae`
                INNER JOIN `Armor` AS `a` ON `a`.`armor_id` = `ae`.`armor_id` 
            WHERE
                `ae`.`equipment_id` = '{player_id}'
        """)

    def get_player_weapons(self, player_id):
        """
        Getting players weapons from DataBase
        :param player_id: Player id
        :return:
        """

        return self.select_query(f"""
            SELECT
                `we`.`weapon_id`,
                `w`.`name` AS `weapon_name`,
                `w`.`price` AS `weapon_price`,
                `w`.`damage_min`,
                `w`.`damage_max`,
                `w`.`weight` AS `weapon_weight`
            FROM
                `Weapon_Equipment` AS `we`
                INNER JOIN `Weapons` AS `w` ON `w`.`id` = `we`.`weapon_id` 
            WHERE
                `we`.`equipment_id` = '{player_id}'
        """)

    def get_player_animals(self, player_id):
        """
        Getting players animals from DataBase
        :param player_id: Player id
        :return:
        """

        return self.select_query(f"""
            SELECT
                `ae`.`animal_id`,
                `a`.`name` AS `animal_name`,
                `a`.`price` AS `animal_price`,
                `a`.`speed` AS `animal_speed`,
                `a`.`capacity` AS `animal_capacity`
            FROM
                `Animals_Equipment` AS `ae`
                INNER JOIN `Animals` AS `a` ON `a`.`animal_id` = `ae`.`animal_id` 
            WHERE
                `ae`.`equipment_id` = '{player_id}'
        """)

    def get_player_attacks(self, class_id, lvl):
        """
        Getting players attacks from DataBase
        :param class_id: Players class id
        :param lvl: lvl
        :return:
        """

        return self.select_query(f"""
            SELECT
                `ca`.`attack_id`,
                `a`.`name` AS `attack_name`,
                `a`.`lvl`,
                `a`.`type_attack`,
                `a`.`count_of_random`,
                `a`.`cooldown`,
                `a`.`random_diapason`,
                `a`.`effect` 
            FROM
                `Classes_Attacks` AS `ca`
                INNER JOIN `Attacks` AS `a` ON `ca`.`attack_id` = `a`.`attack_id` 
            WHERE
                `ca`.`class_id` = '{class_id}' 
                AND `a`.`lvl` <= '{lvl}'
        """)

    def get_player_vulnerabilities(self, player_id):
        """
        Getting players vulnerabilities from DataBase
        :param player_id: Player id
        :return:
        """

        return self.select_query(f"""
            SELECT
                `pv`.`vulnerability_id`,
                `v`.`vulnerability_name`,
                `v`.`vulnerability_description`
            FROM
                `Players_Vulnerabilities` AS `pv`
                INNER JOIN `Vulnerabilities` AS `v` ON `v`.`vulnerability_id` = `pv`.`vulnerability_id` 
            WHERE
                `pv`.`player_id` = '{player_id}'
        """)

    def get_player(self, player_name):
        """
        Getting player info from DataBase
        :param player_name: Player name
        :return:
        """

        main_data = self.get_player_main_data(player_name)
        player_id = main_data[0]['player_id']
        class_id = main_data[0]['class_id']
        lvl = main_data[0]['lvl']

        food = self.get_player_food(player_id)
        armor = self.get_player_armor(player_id)
        weapons = self.get_player_weapons(player_id)
        animals = self.get_player_animals(player_id)
        vulnerabilities = self.get_player_vulnerabilities(player_id)
        attacks = self.get_player_attacks(class_id, lvl)

        return {
            'main': main_data,
            'food': food,
            'armor': armor,
            'weapons': weapons,
            'animals': animals,
            'vulnerabilities': vulnerabilities,
            'attacks': attacks
        }

    def get_dungeon_mobs(self):
        """
        Getting available mobs from DataBase
        :return:
        """

        return self.select_query(f"""  
            SELECT * FROM `Enemies`
        """)

    def get_mobs_attacks(self):
        """
        Getting available mob attacks from DataBase
        :return:
        """

        return self.select_query(f"""
            SELECT ea.enemy_id, `a`.* FROM Enemies_Attacks AS ea
            INNER JOIN Attacks AS a ON a.attack_id = ea.attack_id
        """)

    def get_mobs_vulnerabilities(self):
        """
        Getting available mob vulnerabilities from DataBase
        :return:
        """

        return self.select_query(f"""
            SELECT ev.enemy_id, v.* FROM Enemies_Vulnerabilities AS ev
            INNER JOIN Vulnerabilities AS v ON v.vulnerability_id = ev.vulnerability_id
        """)

    def get_mobs_stats(self):
        """
        Getting available mob stats
        :return:
        """

        return self.select_query(f"""
            SELECT s.* FROM `Enemies` AS `e`
            INNER JOIN Stats AS s ON e.enemy_id = s.hero_id
        """)
