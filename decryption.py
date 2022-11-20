from cryptography.fernet import Fernet


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

# real_decrypt("gAAAAABjemtBMUOJ1OP5Ivl4Bi0mNXjIQyRVZ5xeBovvDFfRQQNJc1gevxZJu34h3dkoS-zqV94M-h0NpW6AIkqppnBEhtIYZ0zjo0hWj-_Hl3tR3JrDYvX4kpeNzNQYr7wjLowHN1LHmMoYadP_6tTv-tDhtPEEsn4EdePfmOS-hOtLpJ4Cuoo17Hla3lq9iq9mazX5m5Ii5k6dUk1fImejHAAfUKfKkoyxiRIg5GadIMv1ylJoPTcf6RkslkmeuAoUGUBjTqcrSWROzJJaD5u19_Zytln-JguGUptrIQ91jRHKhochLgEFv3v4mvRQUnK-ULVMHbzcc-TsRdCMOEKv0f8ea0Sk12V56_c8zv9YRoAWXTr4DG0DvSmPPCAyilY26MuD8rW9iqD_-NBgFdqgUEtbTuRxS21PkIk3rhLv3cyfgYq_jv4NvDX63VirzgEsbtYI2K_K")