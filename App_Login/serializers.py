from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id","username", "email","roles","password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        user = models.User.objects._create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            roles=validated_data['roles']
        )
        return user

class MyAdminProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    profile_pic=serializers.SerializerMethodField()

    class Meta:
        model = models.AdminProfile
        fields = '__all__'

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        profile_pic = obj.profile_pic.url
        return request.build_absolute_uri(profile_pic)


class CustomerProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    profile_pic=serializers.SerializerMethodField()

    class Meta:
        model = models.Customer
        fields = ("id","user", "profile_pic","full_name","phone","address")

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        profile_pic = obj.profile_pic.url
        return request.build_absolute_uri(profile_pic)


class CustomCustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = models.Customer
        fields = ("user",)

class StaffProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    profile_pic=serializers.SerializerMethodField()

    class Meta:
        model = models.Staff
        fields = ("id","user", "profile_pic","full_name","phone","address",'is_verified')

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        profile_pic = obj.profile_pic.url
        return request.build_absolute_uri(profile_pic)

        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role']=user.roles
        token['isAdmin']=user.is_staff
        return token