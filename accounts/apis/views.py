from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from accounts.apis.serializers import UserProfileSerializer


class UserViewSet(viewsets.ViewSet):
  queryset = User.objects.all()
  serializer_class = UserProfileSerializer

  def retrieve(self, request, pk=None):
    if pk == "current":
      user = get_object_or_404(self.queryset, pk=request.user.id)
      serializer = UserProfileSerializer(user)
      return Response(serializer.data)
    else:
      user = get_object_or_404(self.queryset, pk=pk)
      serializer = UserProfileSerializer(user)
      return Response(serializer.data)


# class UsersViewSet(generics.GenericAPIView, ModelViewSet):
#   model = User
#   serializer_class = UserProfileSerializer
#
#   def get_object(self):
#       return self.request.user
#
#   def list(self, request, *args, **kwargs):
#       return self.retrieve(request, *args, **kwargs)
