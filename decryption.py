from cryptography.fernet import Fernet


# Function to load the key
def call_key():
    """
    function to load key
    returns : key
    """
    return open("pass.key", "rb").read()


def real_decrypt(value):
    """
    function to decrypt
    value: required , encrypted string
    return: decrypted data
    """
    key = call_key()
    value = value.encode()
    a = Fernet(key)
    decoded_value = a.decrypt(value)
    print(decoded_value.decode())

# real_decrypt("")