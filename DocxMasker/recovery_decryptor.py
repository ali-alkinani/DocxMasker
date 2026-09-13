# recovery_decryptor.py
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def decrypt_recovery_file(path_file: str, password: str, output_path: str) -> bool:
    try:
        with open(path_file, "rb") as f:
            payload = f.read()

        if len(payload) < 28:
            print("⚠️ Invalid encrypted recovery file structure.")
            return False

        salt_from_file = payload[:16]
        nonce_from_file = payload[16:28]
        ciphertext = payload[28:]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_from_file,
            iterations=700_000,
        )
        key_dec = kdf.derive(password.encode("utf-8"))

        aesgcm = AESGCM(key_dec)
        decrypted_data = aesgcm.decrypt(nonce_from_file, ciphertext, None)

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        return True

    except Exception as e:
        print(f"⚠️ Password is incorrect. Please try again.")
        print(f"   Technical details: {e}")
        return False
