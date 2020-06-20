import json
import pprint
import hashlib
import random

from src.DB.DBCore import DBCore
from src.Modules.DungeonSkeleton import DungeonSkeleton
from src.Modules.UserModule import UserModule
from src.Modules.BattleModule import BattleModule


def main():
    cursor = DBCore()
    test = dict
    player = UserModule(player_data=cursor.get_player("Stas"))
    battle = BattleModule(player=player,
                          battle_data={
                              "player_attack_id": 4,
                              "mob" :
                                  {"attacks":
                                       {
                                           "2": {
                                               "cooldown": 2,
                                               "count_of_random": 3,
                                               "effect": "charm",
                                               "lvl": 1,
                                               "name": "Blessing",
                                               "random_diapason": 6,
                                               "type_attack": "Long Range"
                                           },
                                           "3": {
                                               "cooldown": 10,
                                               "count_of_random": 0,
                                               "effect": "necromancy",
                                               "lvl": 3,
                                               "name": "Reincarnation",
                                               "random_diapason": 0,
                                               "type_attack": "Melee"
                                           }
                                       },
                                      "desc": "Small Plant",
                                      "inventory": {},
                                      "name": "Branchy Infection",
                                      "stats": {
                                          "armor_class": 2,
                                          "chance": 0.0,
                                          "constitution": 3.0,
                                          "dexterity": 8.0,
                                          "hits": 3,
                                          "intelligence": 6.0,
                                          "speed": 4.0,
                                          "strength": 5.0,
                                          "wisdom": 9.0
                                      },
                                      "vulnerabilities": {
                                          "6": {
                                              "vulnerability_description": "Vulnerability to fire damage.",
                                              "vulnerability_name": "Fire"
                                          }
                                      }
                                  }
                          })

    try:
        # player = cursor.get_player_animals(player_id=1)
        pprint.pprint(battle.battle_result())

    except KeyboardInterrupt as e:
        cursor.disconnect()

    cursor.disconnect()


def testing_something():
    graph = {
        "rooms": [0, 1, 2, 3, 4, 5, 6],
        "routes": [
            [0, 1], [0, 4], [1, 2], [1, 5], [2, 3], [2, 5], [2, 6], [3, 5], [5, 6]
        ]
    }
    adj_matrix = {x: [] for x in graph.get('rooms')}
    pprint.pprint(adj_matrix)
    for room in adj_matrix:
        for route in graph.get('routes'):
            pass


if __name__ == '__main__':
    # testing_something()
    main()
