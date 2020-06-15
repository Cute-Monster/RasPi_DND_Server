import hashlib
import json

codes = {
    100: "successfully connected",

    200: "request success",
    201: "dungeon skeleton generated successfully",
    202: "player successfully registered",
    203: "successfully authorized",
    204: "loot generated successfully",
    205: "battle successful",

    400: "server error",
    401: "invalid json format",
    402: "failed to check user",
    403: "action error",
    405: "player name already taken",
    406: "you are not logged",
    407: "player not logged now",
    408: "wrong username or password",
    409: "player already logged",
    410: "no completed dungeon "
}

response = {
    'action': None,
    'code': None,
    'code_desc': None,
    'data': None,
}


def generate_response(action=None,
                      code=None,
                      data=None) -> bytes:
    """
    Method to generate response
    :param action: Invoked action
    :param code: Response code
    :param data: Response data
    :return: String converted to bytes encoded to "utf8"
    """

    global codes
    global response

    response['action'] = action
    response['code'] = code
    response['code_desc'] = codes.get(code)
    response['data'] = data if data else 0

    # json.dumps(response)

    return bytes(
        str(json.dumps(response)),
        "utf8"
    )


def serialize_data(data,
                   column: str
                   ) -> dict:
    """
    Method for serializing user data taken from DataBase
    :param data: Data to serialize
    :param column: Column name
    :return:
    """

    end_data = {}

    for items in data.get(column):
        item_id = items[list(items)[0]]

        del items[list(items)[0]]
        end_data[item_id] = items

    return end_data


def encrypt_password(player_password: str):
    """
    Method for encrypting user password using salt
    :param player_password: User password to encrypt
    :return: Encrypted password
    """

    salt = 'c;]¥Îdå<}Òux¶zCnÖÉóL×ð«&hBè~§Á[ÃF¡v©"Õ,(/P,' \
           'M}Dbëç³çÚ^}°*çµ¹rbÔÁi)xÚè¨2iûÿVLE9)®8ó¥ðt@Ô.]×nïf"ÏC`vzínÑÁpFôwVWÆ6;á©>_À¼mjû¿úõM\'R:7 '

    return hashlib.md5(
        bytes(
            "{}".format(salt + player_password),
            "utf-8"
        )
    ).hexdigest()
