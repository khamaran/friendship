from django.db import models

FOLLOWING_CHOICES = (
        ('Outgoing request', 'Исходящая заявка'),
        ('Incoming request', 'Входящая заявка'),
    )

FRIENDS_CHOICES = (
        ('Friend', 'Друг'),
        ('No friends', 'Не в друзьях'),
)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    objects = models.Manager()
    friends = models.ManyToManyField('self', related_name='comrades',
                                     verbose_name='Друзья',
                                     through='Friends',
                                     symmetrical=False)
    followers = models.ManyToManyField('self', related_name='incoming_requests',
                                       verbose_name='Заявки',
                                       through='Followers',
                                       symmetrical=False)
    status_friends = models.CharField(max_length=50, choices=FRIENDS_CHOICES)
    status_followers = models.CharField(max_length=50, choices=FOLLOWING_CHOICES)

    def __str__(self):
        return self.username


class Friends(models.Model):
    objects = models.Manager()
    person = models.ForeignKey(Profile, related_name='person', on_delete=models.CASCADE)
    friend = models.ForeignKey(Profile, related_name='friend', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person', 'friend')


class Followers(models.Model):
    objects = models.Manager()
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')