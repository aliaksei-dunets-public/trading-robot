import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from app.core.config import settings


class EncryptionTool:
    @staticmethod
    def __generate_open_key(user_id: str, user_token: str = None) -> bytes:
        token = user_token if user_token else user_id

        open_key = settings.ENCRYPT_OPEN_KEY
        if not open_key:
            raise Exception(
                f"EncryptionTool: ENCRYPT_OPEN_KEY is not maintained")

        encode_token = token.encode()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,
            salt=open_key.encode(),
            length=32,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(encode_token))
        return key

    @staticmethod
    def encrypt_key(user_id: str, key: str, user_token: str = None) -> bytes:
        cipher_suite = Fernet(
            key=EncryptionTool.__generate_open_key(user_id, user_token))
        encrypted_api_key = cipher_suite.encrypt(key.encode())
        return encrypted_api_key

    @staticmethod
    def decrypt_key(user_id: str, encrypted_key: bytes, user_token: str = None) -> str:
        cipher_suite = Fernet(
            key=EncryptionTool.__generate_open_key(user_id, user_token))
        decrypted_api_key = cipher_suite.decrypt(encrypted_key).decode()
        return decrypted_api_key
