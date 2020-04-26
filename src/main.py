import sys
from os import path
from Classes import MySQLModule as classes
from Classes.DBCore import DBCore as dbcur
if __name__ == '__main__':
    # path = path.abspath('logs')
    # print(path)
    # error_log_file = open("src/logs/errors.log", "w")
    # with open(r"config.txt", "r+") as file:
    # with open(r"../config.json", "r+") as file:
        # creating connection to the database
    # connection = classes.Connection()
    cursor = dbcur()
    testing_cursors = cursor.get_armor()
    print(*testing_cursors, sep='\n')
    # connection.test_cursor()
    cursor.disconnect()
