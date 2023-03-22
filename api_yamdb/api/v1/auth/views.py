from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import TokenSerializer, SignUpSerializer

User = get_user_model()

DOMAIN_NAME = 'server@yamdbmail.com'


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
        )

        token = default_token_generator.make_token(user)
        send_mail(
            subject='token',
            message=token,
            from_email=DOMAIN_NAME,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(request.data,
                        status=status.HTTP_200_OK,
                        headers=headers,
                        )


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = {
            'access_token': serializer.validated_data['access_token'],
            'refresh_token': serializer.validated_data['refresh_token'],
        }
        return JsonResponse(data=response_data)
