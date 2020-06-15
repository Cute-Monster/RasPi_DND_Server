"""
LootModule.py: Module for generating loot to the user
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

import random
from .UserModule import UserModule


class LootModule:
    """
    Class representing loot module generator
    """

    def __init__(self,
                 dungeon: dict,
                 player: UserModule,
                 loot: dict
                 ):
        self.dungeon = dungeon
        self.loot = loot
        self.player = player

    def _get_random_exp(self,
                        mob: dict
                        ) -> int:
        """
        Generate random experience value depending on mob level
        :param mob: Mob info
        :return:
        """

        try:
            return random.randint(
                mob['mob_level'] * round(
                    random.random() * random.randint(10, 99)
                ),
                mob['mob_level'] * round(
                    random.random() * random.randint(100, 999)
                )
            )
        except ValueError:
            return self._get_random_exp(mob)

    def _set_item_level(self) -> int:
        """
        Generate random level depending on players level
        :return:
        """

        return 1 if self.player.level - 2 < 1 else random.choice(
            range(
                self.player.level - 2,
                self.player.level + 2
            )
        )

    def get_loot(self) -> dict:
        """
        Method to generate loot
        :return: Dictionary containing generated loot by category
        """

        final_weapons = {}
        final_armor = {}
        final_food = {}

        exp = 0
        count_rooms = len(self.dungeon['mobs'])
        count_weapons = random.randint(3 if count_rooms - 3 < 3 else count_rooms, count_rooms + 1)
        count_food = random.randint(5 if count_rooms - 5 < 5 else count_rooms, count_rooms + 10)
        count_armor = random.randint(2 if count_rooms - 6 < 2 else count_rooms, count_rooms)

        item_id = 0
        for uid, room in self.dungeon['mobs'].items():
            mob_counter = len(room)
            for mob_id, mob in room.items():
                exp += round(self._get_random_exp(mob) / mob_counter)

            if count_weapons-1 > len(final_weapons):
                final_weapons[item_id] = self._generate_item(
                    item_type="weapons"
                )

            if count_food > len(final_food):
                final_food[item_id] = self._generate_item(
                    item_type="food")

            if count_armor-1 > len(final_armor):
                final_armor[item_id] = self._generate_item(
                    item_type="armor"
                )

            item_id += 1

        return {
            "level": exp,
            "armor": final_armor,
            "weapons": final_weapons,
            "food": final_food
        }

    def _generate_item(self, item_type: str) -> dict:
        """
        Generate item for loot
        :param item_type: Type of generated item
        :return dict: Item
        """
        item = random.choice(self.loot[item_type]).copy()
        del item[f'{item_type}_id']
        item['lvl'] = self._set_item_level()
        return item
