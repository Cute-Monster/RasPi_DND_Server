import sys
from Classes import Connection as classes
if __name__ == '__main__':
    with open(r"Classes/configs/config.txt", "r+") as file:
        # creating connection to the database
        connection = classes.Connection(file)

    connection.test_cursor()
    connection.disconnect()
