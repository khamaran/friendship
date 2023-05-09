from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ProfileViewSet, FriendsViewSet, \
    FollowersViewSet

router = SimpleRouter()
router.register('profiles', ProfileViewSet, basename='profiles')
router.register(r'profiles/(?P<profile_id>\d+)/friends',
                FriendsViewSet, basename='friends'),
router.register(r'profiles/(?P<profile_id>\d+)/followers',
                FollowersViewSet, basename='followers'),

registration = ProfileViewSet.as_view({'get': 'create'})

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', registration),
]
