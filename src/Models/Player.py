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

from typing import Dict
from .Entity import Entity


class Player(Entity):
    """
    Base Player class
    """
    def __init__(self):
        super().__init__()

        self.player_id = int
        self.player_name = str
        self.class_id = int
        self.race_id = int

        self.food = {}
        self.armor = {}
        self.weapons = {}
        self.animals = {}
        self.vulnerabilities = {}
        self.attacks = {}

    def get_player(self) -> dict:
        """
        Getting all player based info
        :return:
        """

        return self.__dict__