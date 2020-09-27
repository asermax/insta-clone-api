from django.contrib import auth
from django.db import models


class Follow(models.Model):
    following = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
        related_name='followers',
    )
    follower = models.ForeignKey(
        auth.get_user_model(),
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.follower} follows {self.following}'
