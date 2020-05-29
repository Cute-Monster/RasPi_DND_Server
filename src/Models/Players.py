"""
Player.py: Module for representing base Player class
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghosatshow@yandex.ru "
__status__ = "Developing"

import json

from src.Models.Entity import Entity

__all__ = ["Players"]


class Players(Entity):
    """
    Base Player class
    """
    def __init__(self):
        super().__init__()

        self.player_id = None
        self.player_name = None
        self.class_id = None
        self.race_id = None

        self.food = {}
        self.armor = {}
        self.weapons = {}
        self.animals = {}
        self.vulnerabilities = {}
        self.attacks = {}

    def get_player(self) -> str:
        """
        Getting all player based info
        :return:
        """

        return self.__dict__

    # TODO finish this class
