import sys
from Classes import Connection as classes
if __name__ == '__main__':
    # error_log_file = open("src/logs/errors.log", "w")
    # with open(r"config.txt", "r+") as file:
    # with open(r"../config.json", "r+") as file:
        # creating connection to the database
    connection = classes.Connection()
    testing_cursors = connection.cursor.get_armor()
    print(*testing_cursors, sep='\n')
    # connection.test_cursor()
    connection.disconnect()
