"""Users serializers"""

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Django REST Framework Simple JWT
from rest_framework_simplejwt.tokens import RefreshToken

# App imports
from app.users.models import User, Profile
from app.utils.jwt.manuallyTokens import VerificationUserToken
from app.users.serializers.profiles import ProfileModelSerializer

# Tasks
from app.taskapp.tasks import SendConfirmationEmail

# Exceptions
from app.utils.exceptions.users import UserAlreadyVerified


class UserModelSerializer(serializers.ModelSerializer):
    """User Model Serializer"""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
        ]


class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        self.context['user'] = user
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.verified:
            raise serializers.ValidationError("User isn't verified")
        return data

    def create(self, data):
        """Return user with its token credential"""
        user = self.context['user']
        refresh = RefreshToken.for_user(user)
        return user, {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer

    Create an user, profile and send email confirmation
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    username = serializers.CharField(
        max_length=20,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999. Up to 25 digits allowed.'
    )

    phone_number = serializers.CharField(
        max_length=17,
        validators=[phone_regex]
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(max_length=30, min_length=2)
    last_name = serializers.CharField(max_length=30, min_length=2)

    def validate(self, data):
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password)
        return data

    def create(self, data):
        """Handle user and profile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, verified=False, is_client=True)
        Profile.objects.create(user=user)
        SendConfirmationEmail().delay(user.pk)
        return user


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer

    Verify a user with a JWT type email_verification
    """

    token = serializers.CharField()

    def validate(self, data):
        decoder = VerificationUserToken()
        try:
            payload = decoder.decode(data['token'])
        except Exception as e:
            raise serializers.ValidationError(str(e))
        self.context['jwt_payload'] = payload
        return data

    def save(self):
        """Update user's verify status"""
        jwt_payload = self.context['jwt_payload']
        user = User.objects.get(id=jwt_payload['user'])
        if not user.verified:
            user.verified = True
        else:
            raise UserAlreadyVerified()
        user.save()
