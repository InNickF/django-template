"""Users urls"""

# Django imports
from django.urls import path, include

# Django REST Framework imports
from rest_framework.routers import DefaultRouter

# App imports
from app.users.views import AuthUserViewSet, UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'auth', AuthUserViewSet, basename='auth')
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls))
]
