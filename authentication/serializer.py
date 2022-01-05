from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from itapi.models import City

from itapi.serializers import CitySerializer


class FilterSerializer(serializers.Serializer):
    filter = serializers.DictField(required=False)
    sort_by = serializers.CharField(required=False)
    sort_type = serializers.IntegerField(required=False)
    per_page = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)


class RegisterSrializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), many=False)
    extra_kwargs = {
        'city': {'required': True}
    }


class LoginSrializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UpdateSrializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)


class DeleteSrializer(serializers.Serializer):
    password = serializers.CharField()


class RefreshTokenSrializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AddressSrializer(serializers.Serializer):
    name = serializers.CharField()
    stat = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    neighborhood = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    alley = serializers.CharField(required=False)
    house_number = serializers.CharField(required=False)
    others = serializers.JSONField(required=False)


class CompanySrializer(serializers.Serializer):
    name = serializers.CharField()
    economic_code = serializers.CharField(required=False)
    national_code = serializers.CharField(required=False)
    registeration_id = serializers.CharField(required=False)
    telephone_number = serializers.CharField(required=False)
    field_of_activity = serializers.CharField(required=False)


class SocialMediaSerializer(serializers.Serializer):
    facebook = serializers.CharField()
    twitter = serializers.CharField(required=False)
    linkedIn = serializers.CharField(required=False)
    youtube = serializers.CharField(required=False)
    aparat = serializers.CharField(required=False)
    instagram = serializers.CharField(required=False)
    telegram = serializers.CharField(required=False)
    others = serializers.JSONField(required=False)


class InfoSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone_number = serializers.CharField(required=False)
    configurations = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    family_name = serializers.CharField(required=False)
    birthday = serializers.CharField(required=False)
    national_id = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    job = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    others = serializers.JSONField(required=False)


class SessionSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    session_id = serializers.CharField(required=False)
    block_status = serializers.CharField(required=False)


class AdminSecuritySerializer(serializers.Serializer):
    question = serializers.CharField()


class AnsewerSecuritySerializer(serializers.Serializer):
    security_question_id = serializers.CharField()
    answer = serializers.CharField()


class Recovery1Serializer(serializers.Serializer):
    username = serializers.CharField()
    last_password = serializers.CharField()


class Recovery2Serializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField()
    security_question_id = serializers.CharField()
    answer = serializers.CharField()
