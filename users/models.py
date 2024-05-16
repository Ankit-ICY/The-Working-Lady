from django.db import models
from django.contrib.auth.models import User



class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    comment = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    post_title = models.CharField(max_length=30)
    post_image = models.ImageField(upload_to='user_photo', null= True, blank = True)
    post_para = models.TextField()

    class Meta:
        ordering = ['-id'] 

