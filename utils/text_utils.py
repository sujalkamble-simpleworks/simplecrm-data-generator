import json
import base64
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend


# --- Base64 Utils ---
def base64encode(data: str) -> str:
    if not isinstance(data, str):
        if isinstance(data, (int, float)):
            data = str(data)
        else:
            raise ValueError("Text to encode must be a string or number")
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")


def base64decode(data: str) -> str:
    if not isinstance(data, str):
        raise ValueError("Input must be string")
    return base64.b64decode(data.encode("utf-8")).decode("utf-8")


# --- Key Derivation ---
def derive_key(passphrase: str, salt: bytes) -> bytes:
    # 999 iterations, SHA-512, 32-byte key (AES-256)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=999,
        backend=default_backend(),
    )
    return kdf.derive(passphrase.encode("utf-8"))


# --- Encrypt ---
def encryptAES(plain_text: str) -> str:
    passphrase = "373632764d5243706c706d6973"
    salt = os.urandom(32)
    iv = bytes([(-99) % 256] * 16)
    key = derive_key(passphrase, salt)

    padder = padding.PKCS7(128).padder()
    padded = padder.update(plain_text.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(padded) + encryptor.finalize()

    data = {
        "amtext": base64.b64encode(encrypted_bytes).decode("utf-8"),
        "slam_ltol": salt.hex(),
        "iavmol": iv.hex(),
    }
    return base64encode(json.dumps(data))


# --- Decrypt ---
def decryptAES(passphrase: str, encrypted_data: str) -> str | None:
    try:
        parsed = json.loads(base64decode(encrypted_data))
        salt = bytes.fromhex(parsed["slam_ltol"])
        iv = bytes.fromhex(parsed["iavmol"])
        encrypted_bytes = base64.b64decode(parsed["amtext"])

        key = derive_key(passphrase, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

        return decrypted.decode("utf-8")
    except Exception as e:
        print("Decryption error:", e)
        return None


# --- Example ---
if __name__ == "__main__":
    pw = "373632764d5243706c706d6973"
    msg = "SimpleCRM@267"

    enc = encryptAES(msg)
    print("Encrypted:", enc)

    dec = decryptAES(pw, "gBGzvvVSoalc+v2bWZya6nJggBmRjXbhKRx/vXTpbBLUOJDqiFtjV8dKm7nfYuFcjyG9LNXc3oEe2C30S+5nN4RN5BOjPPIAHKPNIrBY7RRqEjqp4/ZGt44Uh2uSOQWI4jHlqnwztCXQ4qIa6jK2+dsm1WyRKWodRG5D2dI/7U8Pkmh/dz8dEV440aEto27ySwvM2d4C9Tc83zIGv+9OKLNocmLndeBNWojSc3NbDXI4TpLVnTGp77J8whutctGPFES6MoeuQRwGzVVI8xykHvUK7GGthoVXnGoYO8QGkxJncgNa5WIwxqP/CpIXFRkiZFev6mzfx5rNMuFBdw+umaoajREMOu971fjUr/QX7jdCm0Cxdqafoxf3Lgu5GkHAoEMzl0HJoYQ6Tm4vL8UN/FNAcUATDAFuLMyeUZyTW695AeAFn2mHV3jtLc0belZWsn4O/Cfb4rxqQtEV1bSlVesAV+ALzqFuz+pthvOj4bqUjPXJCTgZxypdyfrK3l6taJXXBuqJfq/ktYtGa7t8vmB3uyHuXNcARK3kXPo44bwc+jMiDOP86462YruhQ3pKxdj0uNnn7uRM3fiGXUNDDrft0/5B+NNMP/fMNCynDl2C6zQDQTx0Th60FvYuRwxCeboOdn5zM2N+uSei5YaDcm/WI6Co29ozcXMGfDy1+ZE=")
    print("Decrypted:", dec)
    
    print(enc == "gBGzvvVSoalc+v2bWZya6nJggBmRjXbhKRx/vXTpbBLUOJDqiFtjV8dKm7nfYuFcjyG9LNXc3oEe2C30S+5nN4RN5BOjPPIAHKPNIrBY7RRqEjqp4/ZGt44Uh2uSOQWI4jHlqnwztCXQ4qIa6jK2+dsm1WyRKWodRG5D2dI/7U8Pkmh/dz8dEV440aEto27ySwvM2d4C9Tc83zIGv+9OKLNocmLndeBNWojSc3NbDXI4TpLVnTGp77J8whutctGPFES6MoeuQRwGzVVI8xykHvUK7GGthoVXnGoYO8QGkxJncgNa5WIwxqP/CpIXFRkiZFev6mzfx5rNMuFBdw+umaoajREMOu971fjUr/QX7jdCm0Cxdqafoxf3Lgu5GkHAoEMzl0HJoYQ6Tm4vL8UN/FNAcUATDAFuLMyeUZyTW695AeAFn2mHV3jtLc0belZWsn4O/Cfb4rxqQtEV1bSlVesAV+ALzqFuz+pthvOj4bqUjPXJCTgZxypdyfrK3l6taJXXBuqJfq/ktYtGa7t8vmB3uyHuXNcARK3kXPo44bwc+jMiDOP86462YruhQ3pKxdj0uNnn7uRM3fiGXUNDDrft0/5B+NNMP/fMNCynDl2C6zQDQTx0Th60FvYuRwxCeboOdn5zM2N+uSei5YaDcm/WI6Co29ozcXMGfDy1+ZE=")
