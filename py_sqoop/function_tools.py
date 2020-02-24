import os
from hashlib import sha256
from hmac import HMAC


def encrypt_password(password, salt=None):
    """Hash password on the fly."""
    if salt is None:
        salt = os.urandom(8) # 64 bits.

    assert 8 == len(salt)
    assert isinstance(salt, str)

    password = password.encode('UTF-8')

    assert isinstance(password, str)

    result = password
    for i in range(10):
        result = HMAC(result, salt, sha256).digest()

    return salt + result


def validate_password(hashed, input_password):
    return hashed == encrypt_password(input_password, salt=hashed[:8])


def dict_merge(dic1=None, dic2=None):
    for k, v in dic2.items():
        dic1[k] = v
    return dic1
