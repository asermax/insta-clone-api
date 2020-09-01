from django.contrib import auth
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s post ({self.create_date.isoformat()})'


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description
