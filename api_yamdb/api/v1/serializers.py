from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import validate_username

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all()),
                    ]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[EmailValidator(),
                    UniqueValidator(queryset=User.objects.all()),
                    ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def update(self, instance, validated_data):
        if (self.context.get('view').kwargs.get('username') == 'me'
                and 'role' in validated_data):
            del validated_data['role']
        return super().update(instance, validated_data)
