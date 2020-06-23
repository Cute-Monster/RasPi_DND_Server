"""
BattleModule.py: Module which implements battle system
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

from random import choice, randint
from src.Modules.UserModule import UserModule


class BattleModule:
    """
    Class defining battle module
    """

    def __init__(self,
                 player: UserModule,
                 battle_data: dict
                 ):
        self.player = player
        self.attack_id = battle_data['player_attack_id']
        self.mob = battle_data['mob']

    def battle_result(self) -> dict:
        """
        Method which return result of the battle between player and mob
        :return:
        """

        player_hit_result = self._hit_result("player")
        self.mob['stats']['hits'] -= player_hit_result['damage_given']

        mob_hit_result = self._hit_result("mob")
        self.player.hits -= mob_hit_result['damage_given']

        return {
            "attack": player_hit_result['attack'],
            "mob": self.mob,
            "battle_result": {
                "player_attack": player_hit_result,
                "mob_attack": mob_hit_result,
            }
        }

    @staticmethod
    def _dice(side_counter: int,
              throw_counter: int
              ) -> int:
        """
        Method for rolling dice
        :param side_counter: Number of sides
        :param throw_counter: Number of throws
        :return:
        """

        dices = []
        for _ in (0, throw_counter):
            dices.append(randint(0, side_counter))

        return sum(dices)

    def _hit_result(self,
                    whose_turn: str
                    ) -> dict:
        """
        Method which implements battle between the player and mob
        :param whose_turn: Who is hitting now
        :return:
        """

        dice_result = self._dice(20, 1)

        def player_attack() -> dict:
            """
            Battle behaviour on player move
            :return:
            """

            modifier = 0
            damage_given = 0
            attack = self.player.attacks[self.attack_id]
            if attack['attack_type'] == 'Melee':
                modifier = round((self.player.strength + self.player.dexterity) / 3) - 5
            elif attack['attack_type'] == 'Long Range':
                modifier = round((self.player.strength + self.player.chance) / 3) - 5
            elif attack['attack_type'] == 'Magic':
                modifier = round((self.player.intelligence + self.player.wisdom) / 3) - 5

            if modifier + dice_result < self.mob['stats']['armor_class']\
                    or dice_result == 1:
                attack_successful = False
            else:
                attack_dice = self._dice(attack['random_diapason'], attack['count_of_random'])
                attack_successful = True
                damage_given += attack_dice

                for uid, item in self.player.weapons.items():
                    damage_given += choice(range(item['weapon_damage_min'], item['weapon_damage_max']))
            return {
                "attack": attack,
                "attack_successful": str(attack_successful),
                "damage_given": damage_given,
            }

        def mob_attack() -> dict:
            """
            Battle behaviour on a mob move
            :return:
            """

            modifier = 0
            damage_given = 0
            attack = self.mob['attacks'][choice(list(self.mob['attacks'].keys()))]
            if attack['attack_type'] == 'Melee':
                modifier = round((self.mob['stats']['strength'] + self.mob['stats']['dexterity']) / 3) - 5
            elif attack['attack_type'] == 'Long Range':
                modifier = round((self.mob['stats']['strength'] + self.mob['stats']['chance']) / 3) - 5
            elif attack['attack_type'] == 'Magic':
                modifier = round((self.mob['stats']['intelligence'] + self.mob['stats']['wisdom']) / 3) - 5

            if modifier + dice_result < self.player.armor_class\
                    or dice_result == 1:
                attack_successful = False
            else:
                attack_dice = self._dice(attack['random_diapason'], attack['count_of_random'])
                attack_successful = True
                damage_given += int((attack_dice * 0.3) + (0.1 * self.player.hits))
            return {
                "attack": attack,
                "attack_successful": str(attack_successful),
                "damage_given": damage_given,
            }

        attacks = {
            "player": player_attack,
            "mob": mob_attack
        }
        result = attacks.get(whose_turn)()
        return {
            "attack": result.get('attack'),
            "attack_successful": result.get('attack_successful'),
            "damage_given": result.get('damage_given'),
        }
