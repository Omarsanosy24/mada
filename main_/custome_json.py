import json
import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from django.utils.functional import Promise
from rest_framework.renderers import JSONRenderer

from fixxxo.settings import API_PASSWORD


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


def pkcs7_pad(data):
    """
    تطبيق padding بنمط PKCS7 لتكون البيانات من مضاعفات 128-بت (حجم كتلة AES).
    """
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


# تشفير النص
def encrypt_text(text, password):
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


def make_serializable(obj):
    """
    تحويل الكائنات غير القابلة للتسلسل إلى أنواع قابلة للتسلسل.
    """
    if isinstance(obj, Promise):  # التحقق من الكائنات من النوع __proxy__
        return str(obj)
    elif isinstance(obj, dict):
        return {key: make_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        return str(obj)


class CustomJsonRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if renderer_context:
            request = renderer_context.get("request") if renderer_context else None
            try:
                version = request.version if request else None
                if version == "v2":
                    encryption_password = API_PASSWORD

                    # تحويل البيانات إلى نص JSON
                    # json_data = json.dumps(make_serializable(data))

                    # تشفير البيانات
                    serializable = make_serializable(data)
                    encrypted_data = encrypt_text(serializable, encryption_password)

                    # إرجاع البيانات المشفرة كاستجابة JSON
                    custom_data = {
                        "status": serializable.get("status"),
                        "message": serializable.get("message"),
                        "encrypted_data": encrypted_data,
                    }

                    # تحويل البيانات المعدلة إلى JSON
                    return super().render(custom_data, accepted_media_type, renderer_context)
                else:
                    return super().render(data, accepted_media_type, renderer_context)
            except Exception as e:
                # في حالة حدوث خطأ أثناء التشفير، إرجاع البيانات الأصلية
                return super().render(data, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
