from cryptography.fernet import Fernet
import json


# Generating the key and writing it to a file
# def rewriteengine_key():
#     """
#     function to generate key
#     write key to file
#     """
#     key = Fernet.generate_key()
#     with open("pass11.key", "wb") as key_file:
#         key_file.write(key)
#
#
# rewriteengine_key()


# Function to load the key
def call_key():
    """
    function to load key
    returns : key
    """
    return open("pass.key", "rb").read()


def real_encrypt(value):
    """
    function to encrypt
    value: required
    return: encrypted data
    """
    key = call_key()
    value = json.dumps(value)
    value = value.encode()
    a = Fernet(key)
    coded_slogan = a.encrypt(value)
    return coded_slogan.decode()
