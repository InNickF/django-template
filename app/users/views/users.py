"""Users views"""

# Django
from django.forms.models import model_to_dict

# Django rest framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

# App imports
from app.users.models import User
from app.utils.authentication import SetJWTCookiesInResponseObject
from app.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    ProfileModelSerializer
)

# Permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.users.permissions import IsAccountOwner


class AuthUserViewSet(viewsets.GenericViewSet):
    """Auth user views"""

    @action(detail=False, methods=['post'], url_name='login')
    def login(self, request):
        """User login API"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens_dictionary = serializer.save()
        data = {
            'status': 'OK',
            'user': UserModelSerializer(user).data,
            ** tokens_dictionary,
            'message': 'User logged successfully!'
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login/secure', url_name='login_secure')
    def login_secure(self, request):
        """User cookies login API"""

        # Prevent send another JWT via cookies
        if 'access_token' in request.COOKIES and 'refresh_token' in request.COOKIES:
            data = {
                'status': 'Error',
                'message': 'The user is already logged in.'
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user, tokens_dictionary = serializer.save()
            data = {
                'status': 'OK',
                'user': UserModelSerializer(user).data,
                'message': 'User logged successfully via cookies!'
            }
            response = Response(data, status=status.HTTP_201_CREATED)
            jwtCookiesGenerator = SetJWTCookiesInResponseObject()
            response = jwtCookiesGenerator.generate(tokens_dictionary, response)
            return response

    @action(detail=False, methods=['post'], url_name='signup')
    def signup(self, request):
        """User sign up API"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'status': 'OK',
            'user': UserModelSerializer(user).data,
            'message': 'User created successfully!'
        }

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='user/verify', url_name='verify_account_user')
    def account_verification(self, request):
        """User sign up API"""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'status': 'OK',
            'message': 'User verified successfully!'
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='logout')
    def logout(self, request):
        """User logout API"""
        data = {}

        if 'access_token' in request.COOKIES and 'refresh_token' in request.COOKIES:
            data['status'] = 'OK'
            data['message'] = 'User has logged out!'
            response = Response(data, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
        else:
            data['status'] = 'Error'
            data['message'] = 'User has not logged in.'
            response = Response(data, status=status.HTTP_409_CONFLICT)

        return response

    @action(detail=False, methods=['get'], url_path='user/data', url_name='user_data', permission_classes=[IsAuthenticated])
    def get_user_data(self, request):
        """User logout API"""
        user = request.user
        data = {
            'user': UserModelSerializer(user).data,
        }

        return Response(data, status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    """User viewSet"""
    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'profile']:
            permission_classes = [IsAuthenticated, IsAccountOwner]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """Add extra data"""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        #  Here you can add extra data
        data = {
            'user': response.data,
        }
        response.data = data
        return response

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update user profile"""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)
