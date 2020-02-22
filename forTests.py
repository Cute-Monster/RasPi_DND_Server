import json
import os

if __name__ == '__main__':
    arch = os.system('arch')
    if arch is not "armv71":
        print(arch)
    else:
        print("armv71")
