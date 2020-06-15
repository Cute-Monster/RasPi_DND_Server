"""
UserModule.py: Module which represents user in system
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.2.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

from src.Models.Player import Player
from src.Modules import UtilityModule


class UserModule(Player):
    """
    Class which represents UserModule
    """

    def __init__(self,
                 player_data: dict
                 ):
        super().__init__()
        self.player_id = player_data.get('main')[0]['player_id']
        self.player_name = player_data.get('main')[0]['player_name']
        self.level = player_data.get('main')[0]['lvl']
        self.experience = player_data.get('main')[0]['experience']
        self.class_id = player_data.get('main')[0]['class_id']
        self.class_name = player_data.get('main')[0]['class_name']
        self.race_id = player_data.get('main')[0]['race_id']
        self.race = player_data.get('main')[0]['race']

        self.armor_class = player_data.get('main')[0]['armor_class']
        self.hits = player_data.get('main')[0]['hits']
        self.speed = player_data.get('main')[0]['speed']
        self.strength = player_data.get('main')[0]['strength']
        self.dexterity = player_data.get('main')[0]['dexterity']
        self.intelligence = player_data.get('main')[0]['intelligence']
        self.wisdom = player_data.get('main')[0]['wisdom']
        self.chance = player_data.get('main')[0]['chance']
        self.constitution = player_data.get('main')[0]['constitution']

        self.food = UtilityModule.serialize_data(player_data, 'food')
        self.armor = UtilityModule.serialize_data(player_data, 'armor')
        self.weapons = UtilityModule.serialize_data(player_data, 'weapons')
        self.animals = UtilityModule.serialize_data(player_data, 'animals')
        self.vulnerabilities = UtilityModule.serialize_data(player_data, 'vulnerabilities')
        self.attacks = UtilityModule.serialize_data(player_data, 'attacks')

        self.base_exp_for_level = 300
        self.exp_multiplier = 2.35

    def level_up(self,
                 received_experience: int
                 ) -> dict:
        """
                Method for level up
                :param received_experience:
                :return:
                """

        got_new_level = False
        exp_for_next_level = int(self.base_exp_for_level * (self.level ** self.exp_multiplier))
        if self.experience + received_experience > exp_for_next_level:
            self.level += 1
            self.experience = received_experience - exp_for_next_level
            got_new_level = True
        else:
            self.experience += received_experience
        return {
            "newLevel": got_new_level,
            "currentPlayerLevel": self.level,
            "receivedExperience": received_experience,
            "expForNextLevel": int(self.base_exp_for_level * (
                    self.level ** self.exp_multiplier
            )),
            "currentExperience": self.experience,
        }
