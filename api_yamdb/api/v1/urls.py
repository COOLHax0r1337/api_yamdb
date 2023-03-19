from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from .auth.views import SignUpView, TokenView

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenView.as_view(), name='auth_token'),
]
