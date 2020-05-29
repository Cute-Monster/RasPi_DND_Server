"""
Entity.py: Module for representing base Entity class
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghosatshow@yandex.ru "
__status__ = "Developing"


__all__ = ["Entity"]


class Entity:
    """
    Base class for entity
    """
    def __init__(self):
        # Physical stats
        self.race = None
        self.class_name = None
        self.armor_class = None
        self.hits = None
        self.speed = None
        self.strength = None
        self.dexterity = None
        self.intelligence = None
        self.wisdom = None
        self.chance = None
        self.constitution = None
        # Level stats
        self.level = None
        self.experience = None
