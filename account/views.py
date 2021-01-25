from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from account.models import User
from account.serializers import (
    UserSerializer, UserChangePasswordSerializer
)
from account.permissions import IsOwnerOrReadOnly


class UserCreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserChangePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print(serializer.data.get("old_password"))
            if not user.check_password(serializer.data.get("old_password")):
                raise serializers.ValidationError({"detail": ["Invalid old password"]})
            
            user.set_password(serializer.data.get("new_password"))
            user.save()
        
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
        raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
