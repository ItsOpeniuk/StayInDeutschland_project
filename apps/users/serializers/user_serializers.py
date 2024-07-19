from rest_framework import serializers
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re

from apps.users.models.user_model import User


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user details.

    Fields:
        - name: The user's first name.
        - surname: The user's last name.
        - email: The user's email address.
        - phone: The user's phone number.
        - is_lessor: Boolean indicating if the user is a lessor.

    Methods:
        validate_email(value):
            Checks if the email is already in use by another user.

        validate_phone(value):
            Checks if the phone number is already in use by another user.

        validate_name(value):
            Ensures the name contains only letters.

        validate_surname(value):
            Ensures the surname contains only letters.
    """

    class Meta:
        model = User
        fields = [
            'name', 'surname', 'email', 'phone', 'is_lessor'
        ]

    def validate_email(self, value):
        """
        Validate that the email is not already registered for another user.

        Args:
            value (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            serializers.ValidationError: If the email is already registered.
        """
        user = self.context['request'].user

        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                'This email is already registered.'
            )

        return value

    def validate_phone(self, value):
        """
        Validate that the phone number is not already in use by another user.

        Args:
            value (str): The phone number to validate.

        Returns:
            str: The validated phone number.

        Raises:
            serializers.ValidationError: If the phone number is already in use.
        """
        user = self.context['request'].user

        if User.objects.exclude(pk=user.pk).filter(phone=value).exists():
            raise serializers.ValidationError(
                "This phone number is already in use."
            )

        return value

    def validate_name(self, value):
        """
        Validate that the name contains only letters.

        Args:
            value (str): The name to validate.

        Returns:
            str: The validated name.

        Raises:
            serializers.ValidationError: If the name contains non-letter characters.
        """
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError('Name must contain only letters.')

        return value

    def validate_surname(self, value):
        """
        Validate that the surname contains only letters.

        Args:
            value (str): The surname to validate.

        Returns:
            str: The validated surname.

        Raises:
            serializers.ValidationError: If the surname contains non-letter characters.
        """
        if not re.match(r'^[A-Za-z]+$', value):
            raise serializers.ValidationError('Surname must contain only letters.')

        return value


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
        - email: The user's email address.
        - password: The user's password (write-only).

    Meta:
        - `model`: User
        - `fields`: email, password
        - `extra_kwargs`: password is write-only.
    """

    class Meta:
        model = User
        fields = [
            'email', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Fields:
        - username: The user's username.
        - name: The user's first name.
        - surname: The user's last name.
        - email: The user's email address.
        - phone: The user's phone number.
        - is_lessor: Boolean indicating if the user is a lessor.
        - password: The user's password (write-only).
        - re_password: Password confirmation (write-only).

    Methods:
        validate(attrs):
            Validates user registration data including name, surname, phone, and password.

        create(validated_data):
            Creates a new user with the validated data and hashed password.
    """

    re_password = serializers.CharField(max_length=100, write_only=True, validators=[MinLengthValidator(6)])

    class Meta:
        model = User
        fields = [
            'username', 'name', 'surname', 'email', 'phone', 'is_lessor', 'password', 're_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def validate(self, attrs):
        """
        Validate user registration data.

        Args:
            attrs (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the name, surname, phone, or passwords are invalid.
        """
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

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.

        Args:
            validated_data (dict): The validated data.

        Returns:
            User: The created user instance.
        """
        password = validated_data.get('password')
        validated_data.pop('re_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
