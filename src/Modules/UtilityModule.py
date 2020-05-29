import hashlib
import json

codes = {
    100: "successfully connected",
    200: "request success",
    201: "dungeon skeleton generated successfully",
    400: "server error",
    401: "invalid json format",
    402: "failed to check user",
    403: "action error",
    405: "player name already taken",
    406: "player successfully registered",
    407: "you are not logged"
}

response = {
    'action': None,
    'code': None,
    'code_desc': None,
    'data': None,
}


def generate_response(action, code, data=None) -> bytes:
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
    response['data'] = data

    json.dumps(response)

    return bytes(str(response), "utf8")


def serialize_data(data, column: str) -> dict:
    end_data = {}

    for items in data.get(column):
        item_id = items[list(items)[0]]

        del items[list(items)[0]]
        end_data[item_id] = items

    return end_data


def encrypt_password(password: str):
    """
    Method for encrypting user password using salt
    :param password: User password to encrypt
    :return: Encrypted password
    """

    salt = 'c;]¥Îdå<}Òux¶zCnÖÉóL×ð«&hBè~§Á[ÃF¡v©"Õ,(/P,' \
           'M}Dbëç³çÚ^}°*çµ¹rbÔÁi)xÚè¨2iûÿVLE9)®8ó¥ðt@Ô.]×nïf"ÏC`vzínÑÁpFôwVWÆ6;á©>_À¼mjû¿úõM\'R:7 '

    return hashlib.md5(bytes("{}".format(salt + password), "utf-8")).hexdigest()
