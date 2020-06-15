import json
import pprint
import hashlib
import random

from src.DB.DBCore import DBCore
from src.Modules.DungeonSkeleton import DungeonSkeleton
from src.Modules.UserModule import UserModule
from src.Modules.BattleModule import BattleModule


if __name__ == '__main__':

    cursor = DBCore()
    test = dict

    try:
        player = cursor.get_player_animals(player_id=1)
        pprint.pprint(player)

    except KeyboardInterrupt as e:
        cursor.disconnect()

    cursor.disconnect()


