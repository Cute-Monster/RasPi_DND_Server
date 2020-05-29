import json
import pprint

from src.DB.DBCore import DBCore
from src.Modules.DungeonSkeleton import DungeonSkeleton
from src.Modules.UserModule import UserModule
# cursor = None
# import Modules.UtilityModule as Utility

# def __init__():
#     global cursor
#     cursor = dbore()

if __name__ == '__main__':
    # __init__()
    # salt = "9vèQ%+dÞrÒÈµ¤&¡ç4^+:Ã×TvÁxò(RÄpW)Puy9êx¬·b_4«o;åmrbÏ¡&åqêÓ!'>Å"
    # test = "test"
    # print(hashlib.md5(bytes("{}".format(salt + test), "utf-8")).hexdigest())
    # print("78563845fa6c6f5fe37f636b77285c65")
    # print('test'.encode())
    # methods = {
    #     'PlayerAuth': playerAuth
    # }
    # methods.get('')()
    cursor = DBCore()
    test = dict
    # check = UserModule(cursor)
    try:

        # print(check.add("newtest2", "test", 1, 1))

        # print(cursor.add_player("test3", Utility.encrypt_password("test"), 1, 1))
        # print(cursor.get_player("test3").get('main')[0].index(1))
        # check.cursor.disconnect()
        # test.update({"test":5})
        # print(test.keys())
        # print(cursor.check_player_name("test5"))
        player = UserModule(cursor.get_player("test3"))
        # pprint.pprint(player.get_player())
        skeleton = DungeonSkeleton(cursor)
        # skeleton.all_mobs
        pprint.pprint(skeleton.final_dungeon_skeleton(player))
    except KeyboardInterrupt as e:
        cursor.disconnect()

    cursor.disconnect()
    #     check.cursor.disconnect()
    # cursor = dbore()
    # testing_cursors = cursor.get_armor()
    # print(*testing_cursors, sep='\n')
    # connection.test_cursor()
    # cursor.disconnect()

