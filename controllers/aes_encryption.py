from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.backends import default_backend
from fastapi import UploadFile
import os
from constants.files import (
    KEY_PATH,
    ENCRYPTED_FILES,
    DECRYPTED_FILES,
    IV_PATH,
    KEY_PATH_RSA,
)
import base64

from sqlalchemy.orm import Session



async def generate_iv_key():
    random = os.urandom(16)
    return random


async def generate_key():
    random = os.urandom(32)
    return random


def encrypt_from_aes_key(aes_key, data, aes_iv):
    cipher = Cipher(
        algorithms.AES(aes_key), modes.CFB(aes_iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return ciphertext


def decrypt_from_aes_key(aes_key, ciphertext, aes_iv):
    cipher = Cipher(
        algorithms.AES(aes_key), modes.CFB(aes_iv), backend=default_backend()
    )
    decrypter = cipher.decryptor()
    plaintext = decrypter.update(ciphertext) + decrypter.finalize()
    return plaintext


async def generate_aes_key():
    if os.path.exists(KEY_PATH) and os.path.exists(IV_PATH):
        return
    else:
        try:
            iv = await generate_iv_key()
            key = await generate_key()
            with open(IV_PATH, "wb") as iv_file:
                iv_file.write(iv)

            with open(KEY_PATH, "wb") as key_file:
                key_file.write(key)
        except Exception as e:

            print("Error in generating aes key", e)

