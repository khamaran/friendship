from requests import Response
from rest_framework import generics, status, mixins
from rest_framework import viewsets

from .models import Profile, Friends, Followers
from .serializers import ProfileSerializer, \
    FriendsSerializer, FollowersSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class FriendsViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

    def get_queryset(self):
        new_queryset = Friends.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class FollowersViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = Followers.objects.all()
    serializer_class = FollowersSerializer

    def get_queryset(self):
        new_queryset = Followers.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


