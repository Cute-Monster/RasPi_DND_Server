"""
DiceModule.py: Module for rolling dices
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghosatshow@yandex.ru "
__status__ = "Developing"

import random
from src.Logging.Logger import Log

__all__ = ["Dice"]


class Dice:
    """
    Module for rolling dices of specified amount of sides
    """
    def __init__(self):
        self.log_file = Log(self.__class__)
        self.six_side = 6
        self.eight_side = 8
        self.twelve_side = 12
        self.twenty_side = 20

    def roll_six_side_cube(self, times: int) -> list:
        """
        Rolling the six side cube
        :param times: How many times to roll
        :return: List of roll values
        """

        dices = []
        for _ in (0, times-1):
            dices.append(random.randint(self.six_side))
        return dices

    def roll_eight_side_cube(self, times: int) -> list:
        """
        Rolling the eight side cube
        :param times: How many times to roll
        :return: List of roll values
        """

        dices = []
        for _ in (0, times-1):
            dices.append(random.randint(self.eight_side))
        return dices

    def roll_twelve_side_cube(self, times: int) -> list:
        """
        Rolling the twelve side cube
        :param times: How many times to roll
        :return: List of roll values
        """
        dices = []
        for _ in (0, times-1):
            dices.append(random.randint(self.twelve_side))
        return dices

    def roll_twenty_side_cube(self, times: int) -> list:
        """
        Rolling the twelve side cube
        :param times: How many times to roll
        :return: List of roll values
        """
        dices = []
        for _ in (0, times-1):
            dices.append(random.randint(self.twenty_side))
        return dices
    # TODO other dice methods