from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .serializers import SignUpSerializer, TokenSerializer


User = get_user_model()


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        # response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email'],
        )
        headers = self.get_success_headers(serializer.data)
        token = default_token_generator.make_token(user)
        send_mail(
            subject='token',
            message=token,
            from_email='server@yamdbmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        stat = status.HTTP_200_OK
        # if created and (user.email == request.data['email']
        #                 and user.username != request.data['username']):
        #     stat = status.HTTP_400_BAD_REQUEST
        return Response(request.data,
                        status=stat,
                        headers=headers,
                        )


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # confirmation_code = serializer.validated_data['confirmation_code']
        #
        # if not default_token_generator.check_token(user, confirmation_code):
        #     raise ValidationError('Неверный код подтверждения.')
        #
        # jwt_token = RefreshToken.for_user(user)

        response_data = {
            'access_token': serializer.validated_data['access_token'],
            'refresh_token': serializer.validated_data['refresh_token'],
        }
        return JsonResponse(data=response_data)
