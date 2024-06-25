import os, base64
from constants.files import KEY_PATH_RSA
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes


def generate_rsa_keys():
    private_key_rsa = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key_rsa = private_key_rsa.public_key()
    return private_key_rsa, public_key_rsa


async def generate_and_store_rsa_keys():
    new_private_path = KEY_PATH_RSA + "/" + "private_key.key"
    new_public_path = KEY_PATH_RSA + "/" + "public_key.key"
    if not os.path.exists(KEY_PATH_RSA):
        os.makedirs(KEY_PATH_RSA)
    if os.path.exists(new_private_path) or os.path.exists(new_public_path):
        return
    else:
        try:

            private_key, public_key = generate_rsa_keys()
            with open(new_private_path, "wb") as private_key_file:
                private_key = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
                private_key_file.write(private_key)
                private_key_file.close()
            with open(new_public_path, "wb") as public_key_file:
                public_key = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                public_key_file.write(public_key)
                public_key_file.close()
        except Exception as e:
            print("Error in generating rsa key", e)


def read_private_key_from_file():
    private_path = KEY_PATH_RSA + "/" + "private_key.key"

    with open(private_path, "rb") as key_file:

        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )
        key_file.close()
    return private_key


def read_public_key_from_file():
    public_path = KEY_PATH_RSA + "/" + "public_key.key"

    with open(public_path) as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend()
        )
    key_file.close()
    return public_key


async def encrypt_from_rsa_public_key(data: str):
    try:
        data = data.encode()
        public_key = read_public_key_from_file()

        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        ciphertext = base64.b64encode(ciphertext).decode()
        return ciphertext
    except Exception as e:
        print("Error in encrypting from rsa key", e)
        return None


async def encrypt_from_rsa_public_key_string(key: str, data: str):
    try:
        data = str(data)
        data = data.encode()
        key = base64.b64decode(key)
        public_key = serialization.load_pem_public_key(key, backend=default_backend())
        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        ciphertext = base64.b64encode(ciphertext).decode()
        return ciphertext
    except Exception as e:
        print("Error in encrypting from rsa key", e)
        return None


async def decrypt_from_rsa_private_key(data: str):
    try:
        data = base64.b64decode(data)

        private_key = read_private_key_from_file()
        plain_text = private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        plain_text = plain_text.decode()

        return plain_text
    except Exception as e:
        print("Error in decrypting from rsa key", e)
        return ""


async def get_rsa_public_key():
    public_path = KEY_PATH_RSA + "/" + "public_key.key"
    with open(public_path, "rb") as public_key_file:
        public_key = public_key_file.read()
        decoded_public_key = base64.b64encode(public_key).decode()
        return decoded_public_key
