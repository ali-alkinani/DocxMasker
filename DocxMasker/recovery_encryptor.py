# recovery_encryptor.py
import os
import gc
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def encrypt_recovery_file(file_path: str, password: str, path_encrypted: str) -> bool:
    """
    Encrypt a JSON recovery file using AESGCM with PBKDF2HMAC key derivation
    and safely delete the unencrypted original JSON file.
    """
    try:
        if not os.path.exists(file_path):
            print(f"⚠️ Source file not found: {file_path}")
            return False

        if not password or not password.strip():
            print("⚠️ No password provided for encryption.")
            return False

        # قراءة البيانات وإغلاق الملف فوراً
        with open(file_path, "rb") as f:
            file_data = f.read()

        salt = os.urandom(16)
        nonce = os.urandom(12)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=700_000,
        )
        key = kdf.derive(password.encode("utf-8"))

        aesgcm = AESGCM(key)
        encrypted_data = aesgcm.encrypt(nonce, file_data, None)

        # كتابة البيانات المشفّرة
        with open(path_encrypted, "wb") as f:
            f.write(salt + nonce + encrypted_data)

        # تحرير أي قيود على الملف وإزالة الملف الأصلي غير المشفر
        gc.collect()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as del_err:
                print(f"⚠️ Could not delete original json immediately: {del_err}")

        print("✅ Recovery file encrypted successfully.")
        return True

    except Exception as e:
        print(f"⚠️ Error encrypting recovery file: {e}")
        return False
