from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Profile, Friends, Followers


class ProfileSerializer(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True, read_only=True)
    followers = serializers.StringRelatedField(many=True, read_only=True)
    status_friends = serializers.StringRelatedField(many=True, read_only=True)
    status_followers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        many=True,
        queryset=Followers.objects.all()
    )
    status = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Followers
        validators = (
            UniqueTogetherValidator(
                queryset=Followers.objects.all(),
                fields=('follower', 'following',),
                message="Вы уже отправили запрос на подписку этому человеку!"
            ),
        )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data


class FriendsSerializer(serializers.ModelSerializer):
    person = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    friend = serializers.SlugRelatedField(
        slug_field='username',
        many=True,
        queryset=Friends.objects.all()
    )
    status = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Friends
        validators = (
            UniqueTogetherValidator(
                queryset=Followers.objects.all(),
                fields=('person', 'friends',),
                message="Вы уже 'в друзьях' у этого пользователя!"
            ),
        )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя добавить в друзья самого себя!')
        return data
