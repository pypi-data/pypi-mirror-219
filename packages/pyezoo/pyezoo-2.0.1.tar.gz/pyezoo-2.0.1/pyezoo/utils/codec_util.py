import hashlib
import binascii


salt = "ezoo"
iteration = 1000


def key_derive(pwd):
    salt_pwd = hashlib.pbkdf2_hmac('sha1', pwd.encode("utf-8"), salt.encode("utf-8"), 1000)
    return binascii.hexlify(salt_pwd).decode("utf-8")
