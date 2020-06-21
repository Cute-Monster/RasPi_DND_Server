"""
DungeonSkeleton.py: Module for generating dungeon skeleton with mobs for each room
"""
__author__ = "Runtov Constantin, Mandrila Daniel"
__copyright__ = "Copyright 2020, The Earth"
__credits__ = ["Runtov Constantin", "Mandrila Daniel"]
__license__ = "USM"
__version__ = "0.1.5"
__maintainer__ = "Gheorghe Latul"
__email__ = "ghostshow@yandex.ru "
__status__ = "Developing"

import copy
from networkx.generators.random_graphs import erdos_renyi_graph
import random
import pprint
from src.Modules.UserModule import UserModule
from src.DB.DBCore import DBCore
from src.Logging.Logger import Log

class DungeonSkeleton:
    """
    Module which generates random dungeon skeleton with mobs for player
    """

    def __init__(self,
                 cursor: DBCore
                 ):
        self.log_file = Log(
            class_name=self.__class__
        )
        self.cursor = cursor
        self.all_mobs = self._generate_mobs()

    def final_dungeon_skeleton(self, player_data: UserModule) -> dict:
        """
        Create final dungeon structure for a player from:
            1 -> dungeon structure
            2 -> available mobs which are little modified by adding level
        :return: Dictionary representing final dungeon structure for player
        """

        graph_structure = self._generate_graph_structure()

        for room in graph_structure['rooms']:
            graph_structure['mobs'][room] = {}
            for mob_uid in range(0, random.choice([1, 2, 3])):
                mob = copy.deepcopy(self.all_mobs[random.choice(
                    range(
                        1,
                        len(self.all_mobs.keys())
                    )
                )])

                mob['mob_level'] = 1 if player_data.level - 2 < 1 else random.choice(
                    range(player_data.level - 2, player_data.level)
                )

                mob['stats']['hits'] = mob['stats']['hits'] if player_data.level - 2 < 1 else mob['stats']['hits'] * 2.5
                graph_structure['mobs'][room][mob_uid] = mob
        self.log_file.log_all(
            priority=3,
            string=f"Dungeon skeleton filled with mobs"
        )
        return graph_structure

    def _generate_graph_structure(self) -> dict:
        """
        Generate random graph structure with given number of nodes and % of routes
        :return: Dictionary representing graph structure
        """

        nodes_counter = random.choice(range(5, 10))
        percent_of_routes = 0.4
        graph = erdos_renyi_graph(nodes_counter, percent_of_routes)
        edges = []
        for edge in graph.edges:
            edges.append(list(edge))
        self.log_file.log_all(
            priority=3,
            string=f"Dungeon skeleton generated"
        )
        return {
            "rooms": list(graph.nodes),
            "routes": edges,
            "mobs": {}
        }

    def _generate_mobs(self) -> dict:
        """
        Generate mobs from available mobs in the DataBase
        :return: Dictionary of all available mobs
        """

        available_mobs = self.cursor.get_dungeon_mobs()
        all_vulnerabilities = self.cursor.get_mobs_vulnerabilities()
        all_attacks = self.cursor.get_mobs_attacks()
        all_stats = self.cursor.get_mobs_stats()

        generated_mobs = {}

        for mob in available_mobs:

            mob_id = mob[list(mob)[0]]
            mob_attacks = self._mob_data_parser(mob_id, all_attacks)
            mob_vulnerabilities = self._mob_data_parser(mob_id, all_vulnerabilities)
            mob_stats = self._mob_data_parser(mob_id, all_stats, stats_flag=True)
            generated_mobs[mob['enemy_id']] = {
                "name": mob['name'],
                "desc": mob['description'],
                "attacks": mob_attacks,
                "stats": mob_stats,
                "vulnerabilities": mob_vulnerabilities,
                "inventory": {}
            }
            self.log_file.log_all(
                priority=3,
                string=f"Mobs Generated"
            )

        return generated_mobs

    @staticmethod
    def _mob_data_parser(mob_id: int,
                         data: dict,
                         stats_flag=False
                         ) -> dict:
        """
        Parsing data about mobs
        :param mob_id: Id of the mob
        :param data: Data to parse
        :param stats_flag: Flag used to determine if stats dict is being parse
        :return:
        """

        end_data = {}
        for item in data:
            enemy_id = item[list(item)[0]]
            stats_id = item[list(item)[1]]
            temp = item.copy()
            del temp[list(temp)[0]]
            if not stats_flag:
                del temp[list(temp)[0]]
            if mob_id == enemy_id:
                if not stats_flag:
                    end_data[stats_id] = temp
                else:
                    end_data = temp
        return end_data
