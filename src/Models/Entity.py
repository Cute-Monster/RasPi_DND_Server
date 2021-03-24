"""
Entity.py: Module for representing base Entity class
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"


class Entity:
    """
    Base class for entity
    """

    def __init__(self):
        # Physical stats
        self.race: str
        self.class_name: str
        self.armor_class: int
        self.hits: int
        self.speed: float
        self.strength: float
        self.dexterity: float
        self.intelligence: float
        self.wisdom: float
        self.chance: float
        self.constitution: float
        # Level stats
        self.level: int
        self.experience: int
