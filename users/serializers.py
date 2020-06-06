from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django_countries.serializer_fields import CountryField
from products.serializers import BaseProductSerializer
from product_folders.serializers import ProductFoldersSerializer
from product_folders.models import ProductFolders


class UserSerializer(serializers.ModelSerializer):

    country = CountryField

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'profile_picture',
                  'username', 'date_of_birth', 'country', 'bio',
                  'status', 'folders',
                  'datetime_created', 'datetime_last_logout')

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError("Not unique email")
        return norm_email

    def validate_first_name(self, value):
        norm_first_name = value.lower()
        return norm_first_name

    def validate_last_name(self, value):
        norm_last_name = value.lower()
        return norm_last_name

    def to_representation(self, obj):
        data = super(UserSerializer, self).to_representation(obj)
        if data['country'] == '':
            data['country'] = ''
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'bio')

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError("Not unique email")
        return norm_email

    def validate_first_name(self, value):
        norm_first_name = value.lower()
        return norm_first_name

    def validate_last_name(self, value):
        norm_last_name = value.lower()
        return norm_last_name


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'profile_picture',
            'username',
            'bio'
        )

    def validate_first_name(self, value):
        norm_first_name = value.lower()
        return norm_first_name

    def validate_last_name(self, value):
        norm_last_name = value.lower()
        return norm_last_name


# class UserSavedProductsSerializer(serializers.ModelSerializer):

#     saved_products = BaseProductSerializer(many=True)

#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'saved_products'
#         )
