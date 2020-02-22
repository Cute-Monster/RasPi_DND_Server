import sys
from Classes import Connection as classes
if __name__ == '__main__':
    with open(r"../config.json", "r+") as file:
        # creating connection to the database
        connection = classes.Connection(file)

    connection.test_cursor()
    connection.disconnect()
