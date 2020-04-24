import json
import os

if __name__ == '__main__':
    # arch = os.system('arch')
    # if arch is not "armv71":
    #     print(arch)
    # else:
    #     print("armv71")
    from requests import get

    ip = get('https://api.ipify.org').text
    print('My public IP address is:', ip)