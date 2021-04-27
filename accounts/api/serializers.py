from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import exceptions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class LoginSerializer(serializers.Serializer):
    # 验证username和password是否存在
    username = serializers.CharField()
    password = serializers.CharField()


# 此处使用的是ModelSerializer 来实际创建出一个user
class SignupSerializer(serializers.ModelSerializer):
    # 验证用户注册
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()   # 此处使用email field

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    # will be called when is_valid is called
    def validate(self, data):
        if User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': "This username has been occupied"
            })
        if User.objects.filter(email=data['email'].lower()).exists():
            raise exceptions.ValidationError({
                "email": "This email address has been occupied"
            })
        return data

    def create(self, validated_data):
        # 此处使用的是validated_data而不是普通的data
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,

        )
        return user
