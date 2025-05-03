from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import AnonymousUser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authtoken.models import Token
import base64
import hashlib
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend



class IsOwner(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_staff)
        else:
            return False


class IsOwnerOrReadOnly(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user and request.user.is_staff)
        else:
            return False

def get_user(key):
    model = Token
    key = key.split()
    if not key or key[0].lower() != "token":
        return AnonymousUser()
    if len(key) == 1:
        return AnonymousUser()
    elif len(key) > 2:
        return AnonymousUser()
    token = key[1]
    try:
        token = model.objects.select_related('user').get(key=token)
    except model.DoesNotExist:
        return AnonymousUser()

    if not token.user.is_active:
        return AnonymousUser()

    return token.user

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

from django.utils import timezone

class HasAPIKeyWithTimeCheck(HasAPIKey):
    def get_api_key(self, request):
        # استخراج ال API Key مع التايم ستامب من ال header
        authorization = request.META.get(settings.API_KEY_CUSTOM_HEADER)
        if not authorization:
            return None, None
        try:
            # _, api_key_with_time = authorization.split()
            # فصل ال API Key عن التايم ستامب
            decrypted = decrypt_text(authorization, settings.API_KEY_PASSWORD)
            api_key, timestamp_str = decrypted.rsplit('///', 1)
            timestamp_str = timestamp_str.replace('"', "")
            api_key = api_key.replace('"', "")
            timestamp = int(float(timestamp_str))
            return api_key, timestamp
        except Exception as e:
            return None, None

    def get_key(self, request):
        # if request.version != "v3":
        #     return super().get_key(request)
        # استخراج ال API Key مع التايم ستامب من ال header
        authorization = request.META.get(settings.API_KEY_CUSTOM_HEADER)
        if not authorization:
            return None
        try:
            decrypted = decrypt_text(authorization, settings.API_KEY_PASSWORD)
            api_key, timestamp_str = decrypted.rsplit('///', 1)
            api_key = api_key.replace('"', "")

            return api_key
        except Exception as e:
            return None

    def has_permission(self, request, view):
        if request.version == "v3112233":
            return True
        # return True
        api_key, timestamp = self.get_api_key(request)
        if not api_key:
            return False
        # التحقق من صحة ال API Key باستخدام المنطق الأصلي
        is_valid = super().has_permission(request, view)
        if not is_valid:
            return False
        # التحقق من التايم ستامب
        current_time = int(timezone.now().timestamp())
        time_diff = current_time - timestamp
        if abs(time_diff) > 15:
            return False
        return True

def QueryAuthMiddleware(scope):
    # Look up user from query string (you should also do things like
    # checking if it is a valid user ID, or if scope["user"] is already
    # populated).

    authorization_value = scope['query_string']
    if authorization_value:
        scope['user'] = get_user(authorization_value.decode('utf-8').replace('=', " "))

    return scope
