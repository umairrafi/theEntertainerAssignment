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

real_decrypt("gAAAAABje59aU3gcLVaC_Zzv58GHMVcRjbYvq-pKsSMLRb_fjVq3AkDL_Hu6-hktYzztFg3Hv31xkL0LmFgEAJj48T2-EikfqhN_iLL0wAGQE2rS3EH1NfIPRPmc1UCY6eDQdEYxQnPsF7iV3QFbl9xih6nATQYNYAV-xqzR5o0vgC_p_mTWazsxX2GuMI9d_rrciUbwDHa2PcUwd_4lzrLj4tSZ8xz090se4UeT88NKUK-wWsUOI82O3RDF9IbDsYNPWhaYjfJv4BfJB5WfAqsGBkA1_-J_UvLN4j1LgCORn6UMhq7PaElOSciKovv2q03vnYKUZL4uGoI0GXB2Pb91iTfcu0hqbQ==")