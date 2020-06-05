from src.Models.Player import Player
from src.Modules import UtilityModule


class UserModule(Player):
    def __init__(self, player_data):
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
