from rest_framework.parsers import BaseParser
import base64
import hashlib
import json
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.conf import settings


def evp_bytes_to_key(password, salt, key_len, iv_len):
    """
    دالة اشتقاق المفتاح والـ IV كما في OpenSSL باستخدام MD5.
    """
    dtot = b""
    d = b""
    while len(dtot) < key_len + iv_len:
        d = hashlib.md5(d + password + salt).digest()
        dtot += d
    return dtot[:key_len], dtot[key_len:key_len + iv_len]


def pkcs7_unpad(data):
    """
    إزالة padding بنمط PKCS7 بعد فك التشفير.
    """
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data


class DecryptionParser(BaseParser):
    """
    Custom Parser لفك تشفير البيانات الواردة في الطلب.
    """
    # media_type = 'application/x-www-form-urlencoded'  # تحديد نوع البيانات التي يتعامل معها الـ Parser
    media_type = 'application/json'

    def parse(self, stream, media_type=None, parser_context=None):
        # قراءة البيانات المشفرة من الطلب
        encrypted_data = stream.read().decode('utf-8')
        encrypted_bytes = base64.b64decode(encrypted_data)

        # استخراج الـ salt والمحتوى المشفر
        if not encrypted_bytes.startswith(b"Salted__"):
            raise ValueError("Invalid encrypted data format. Expected 'Salted__' prefix.")
        salt = encrypted_bytes[8:16]  # استخراج الـ salt (البايتات من 8 إلى 16)
        encrypted = encrypted_bytes[16:]  # استخراج المحتوى المشفر
        password = "my_password"  # عبارة المرور المستخدمة في التشفير
        # اشتقاق المفتاح والـ IV من عبارة المرور والـ salt
        key, iv = evp_bytes_to_key(password.encode('utf-8'), salt, 32, 16)

        # إنشاء الكائن الخاص بفك التشفير بنمط CBC
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()

        # إزالة padding
        decrypted_data = pkcs7_unpad(decrypted_padded)

        # تحويل البيانات إلى نص JSON ثم إلى كائن Python
        json_string = decrypted_data.decode('utf-8')
        text = json.loads(json_string)

        return text