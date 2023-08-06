import base64
import os

from aiohttp import web
from cryptography.fernet import Fernet


globals_dict = {'app': web.Application()}


def k():
    file_path = os.path.abspath('license.key')
    if not os.path.exists(file_path):
        with open(file_path, "x"):
            print("The license file does not exist.")
            return Fernet.generate_key()
    else:
        with open(file_path, 'r') as f:
            k_str = f.read().split("::::")[0]
            return base64.urlsafe_b64decode(k_str)


def main():
    current_script_path = os.path.abspath(__file__)
    package_directory = os.path.dirname(current_script_path)
    file_path = os.path.join(package_directory, 'files-automl/application.txt')
    with open(file_path, 'rb') as enc_file:
        d = Fernet(k()).decrypt(enc_file.read())
        exec(d, globals_dict)


if __name__ == '__main__':
    main()
