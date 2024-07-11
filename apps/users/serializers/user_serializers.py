from rest_framework import serializers
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re

from apps.users.models.user_model import User


class UserListDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'name', 'surname', 'email', 'phone', 'is_lessor'
        ]


class UserLoginSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = [
            'email', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserRegistrationSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField(max_length=100, write_only=True, validators=[MinLengthValidator(6)])

    class Meta:
        model = User
        fields = [
            'name', 'surname', 'email', 'phone', 'is_lessor', 'password', 're_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

        @staticmethod
        def validate(attrs):
            name = attrs.get('name')
            surname = attrs.get('surname')
            phone = attrs.get('phone')

            if not re.match(r'^[A-Za-z]+$', name):
                raise serializers.ValidationError(
                    {'name': 'Name must be alphanumeric'}
                )

            if not re.match(r'^[A-Za-z]+$', surname):
                raise serializers.ValidationError(
                    {'surname': 'Surname must be alphanumeric'}
                )

            if not re.match(r'^\+49\d{11}$', phone):
                raise serializers.ValidationError(
                    {'phone': 'Phone must be like "+4919117293711"'}
                )

            password = attrs.get('password')
            re_password = attrs.get('re_password')

            if password != re_password:
                raise serializers.ValidationError(
                    {'re_password': 'Passwords must match'}
                )

            try:
                validate_password(password)
            except ValidationError as err:
                raise serializers.ValidationError(
                    {'password': err.messages}
                )

            return attrs

        @staticmethod
        def create(validated_data):
            password = validated_data.get('password')
            validated_data.pop('re_password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()

            return user
