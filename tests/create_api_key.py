import base64
import datetime
import hashlib
import json
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from rest_framework_api_key.models import APIKey


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


def decrypt_text(encrypted_base64, password):
    """
    دالة فك تشفير النص المشفر باستخدام AES-CBC.
    """
    # تحويل النص المشفر من Base64 إلى بايتات
    encrypted_bytes = base64.b64decode(encrypted_base64)

    # استخراج الـ salt والمحتوى المشفر
    if not encrypted_bytes.startswith(b"Salted__"):
        raise ValueError("Invalid encrypted data format. Expected 'Salted__' prefix.")
    salt = encrypted_bytes[8:16]  # استخراج الـ salt (البايتات من 8 إلى 16)
    encrypted = encrypted_bytes[16:]  # استخراج المحتوى المشفر

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
    return json_string

def pkcs7_pad(data):
    """
    تطبيق padding بنمط PKCS7 لتكون البيانات من مضاعفات 128-بت (حجم كتلة AES).
    """
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


# تشفير النص
def encrypt_text(text, password):
    text = f"{text}///{datetime.datetime.now().timestamp()}"
    json_string = json.dumps(text)
    json_bytes = json_string.encode('utf-8')
    # تطبيق PKCS7 padding
    padded_data = pkcs7_pad(json_bytes)
    # توليد salt عشوائي (8 بايت كما في OpenSSL)
    salt = os.urandom(8)
    # اشتقاق المفتاح والـ IV من عبارة المرور والـ salt
    key, iv = evp_bytes_to_key(password.encode('utf-8'), salt, 32, 16)
    # إنشاء الكائن الخاص بالتشفير بنمط CBC باستخدام مكتبة cryptography
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    # إضافة بادئة "Salted__" والـ salt كما يفعل OpenSSL
    encrypted_bytes = b"Salted__" + salt + encrypted
    # تحويل النتيجة إلى Base64 للحصول على سلسلة نصية متوافقة مع CryptoJS
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_base64

# password = "gyyny8oloaarg3hlmksmhmtrtrtrfkrnyarg3a7bhmksmhmtrtrtrmsrhyamynylhahodmylogyfyrgo3ansanytmlym3ak"
# print(f"ydTf0dBl.aZWCWH2bkzEjb1rAJfB8X7wF1tpk0qaR///{datetime.datetime.now().timestamp()}")
# text = {"token": f"ydTf0dBl.aZWCWH2bkzEjb1rAJfB8X7wF1tpk0qaR///{datetime.datetime.now().timestamp()}", "number": 123}
# encrypted = "U2FsdGVkX19Q+AR21Q2fY4Uf2T0NKs5Hz15dGTpzl04="
# encrypted2 = encrypt_text(text, password)
# print("Encrypted:", encrypted)
# print("Encrypted2:", encrypted2)
# decrypted = decrypt_text(encrypted, password)
# print("Decrypted:", decrypted, datetime.datetime.now().timestamp())


def get_api_key():
    obj, api_key = APIKey.objects.create_key(name="test", prefix="test")
    return encrypt_text(api_key, settings.API_KEY_PASSWORD)
