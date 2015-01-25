from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from mail.models import Mail, MailAttachment, MailForward

from advertisement.models import UserProfile

from .models import Country


class RegistrationSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()
    password1 = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    avatar = serializers.ImageField(required=False)
    country = serializers.CharField(required=True)
    # password2 = serializers.CharField()

    def validate_phone_number(self, attrs, phone_number):
        phone_number = attrs[phone_number]

        if User.objects.filter(username=phone_number, is_active=True).exists():
            raise serializers.ValidationError('User with that phone number already exists.')
        return attrs

        # def validate(self, attrs):
        # password1 = attrs['password1']
        #     password2 = attrs['password2']
        #
        #     if password1 != password2:
        #         raise serializers.ValidationError("Two password fields doesn't matches.")
        #
        #     return attrs


class PhoneNumberValidationSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()
    secret_token = serializers.IntegerField()


class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail


class MailForwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailForward
        fields = ('email', 'title')


class MailForwardSerializerDestroy(serializers.ModelSerializer):
    class Meta:
        model = MailForward
        fields = ('email',)


class UserLinkedMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserLinkedMailSerializer(read_only=True)

    class Meta:
        model = UserProfile


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'code', 'prefix')


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, attrs, username):
        username = attrs[username]
        if not User.objects.filter(username=username, is_active=True).exists():
            raise serializers.ValidationError("User with that username doesn't exists or is inactive.")
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    oldpassword = serializers.CharField()
    newpassword = serializers.CharField()
