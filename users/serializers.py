from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
import ipdb

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all(), message='username already taken.')],
    )
    email = serializers.EmailField(
        max_length=127,
        validators=[UniqueValidator(queryset=User.objects.all(), message='email already registered.')],
    )
    birthdate = serializers.DateField(default=None)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    is_employee = serializers.BooleanField(default=False)
    id = serializers.IntegerField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    

    def create(self, validated_data):
        
        if validated_data['is_employee']:
            user = User.objects.create_superuser(**validated_data)    

        else:
            user = User.objects.create_user(**validated_data)
        
        return user
    