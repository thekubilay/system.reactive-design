from rest_framework import serializers
from rest_auth.serializers import TokenSerializer
from django.contrib.auth.models import User


class UserTokenSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id',)


class CustomTokenSerializer(TokenSerializer):
  user = UserTokenSerializer(read_only=True)

  class Meta(TokenSerializer.Meta):
    fields = ('key', 'user')


class UserProfileSerializer(serializers.ModelSerializer):
  extra_data = serializers.SerializerMethodField(read_only=True)
  is_superuser = serializers.BooleanField(read_only=True)
  is_staff = serializers.BooleanField(read_only=True)

  class Meta:
    model = User
    fields = ("id", "username", "first_name", "last_name", "is_superuser", "is_staff", "email", "extra_data")
    depth = 1

  def get_extra_data(self, instance):
    if instance.is_superuser is not True:
      extra_data = instance.socialaccount_set.all()[0].extra_data
      return extra_data
