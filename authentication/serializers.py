from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed


# import magic


# load_dotenv()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    email = serializers.EmailField(max_length=68, min_length=6)

    class Meta:
        model = User
        fields = [
            "email",
            "password", "first_name",
            "token", "last_name",
            "id"

        ]

    def validate(self, attrs):
        email = attrs.get('email', None)
        if User.objects.filter(email=email.lower()).exists():
            raise serializers.ValidationError({
                "email": _("this email is already exist")
            })

        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )

        return user


class UserBetaSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', "email", "last_name", "id",
        ]


class UserInfoSer(UserBetaSer):
    pass


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=2000, min_length=3, read_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    data = serializers.JSONField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email", "data",
            "id", "password",
            "token"
        ]

    def validate_email(self, attrs):
        email = attrs.lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("User does not exist."))
        return attrs

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password", None)
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"password": _("incorrect password")})
        tt, token = Token.objects.get_or_create(user=user)
        data = UserInfoSer(instance=user, context=self.context).data
        return {
            "token": tt.key,
            "data": data,
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True, required=False)
    email = serializers.EmailField(min_length=2, write_only=True)
    otp = serializers.CharField(min_length=4, write_only=True)

    class Meta:
        fields = ["password", "email", "otp"]

    def validate(self, attrs):
        try:
            password = attrs.get("password", False)
            email = attrs.get("email")
            otp = attrs.get("otp")
            user = User.objects.get(email=email)
            from django.utils import timezone
            if user.otp.filter(otp=otp, expire__gt=timezone.now(), is_used=False).exists():
                if password:
                    user.otp.filter(otp=otp, expire__gt=timezone.now(), is_used=False).update(is_used=True)
                    user.set_password(password)
                    user.save()
                return user
            raise AuthenticationFailed("The otp is invalid", 401)
        except Exception as e:
            raise AuthenticationFailed("The otp is invalid", 401)


#
#


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()
    default_error_messages = {"bad_token": _("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["token"]
        return attrs

    def save(self, **kwargs):
        try:
            Token.objects.get(key=self.token).delete()
        except:
            self.fail("bad_token")


class ChangePasswordSer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6, write_only=True)
    new_password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password', None)

        user = self.context['request'].user
        if user.check_password(old_password):
            return attrs
        raise serializers.ValidationError({"old_password": _("incorrect password")})

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
