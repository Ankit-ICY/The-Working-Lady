from django.db import models
from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField

from tinymce.models import HTMLField


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    comment = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    

class Post(models.Model):
    post_title = models.CharField(max_length=30)
    post_image = models.ImageField(upload_to='resumes', null= True, blank = True)
    post_para = models.TextField()

    class Meta:
        ordering = ['-id'] 




class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = HTMLField()
    author = models.CharField(max_length=30, default='',null= True, blank = True)
    image = models.ImageField(upload_to='resumes', null= True, blank = True)
    description = models.TextField(default='',null= True, blank = True)
    date = models.DateField(auto_now_add=True, null=True)


    def __str__(self) -> str:
        return self.title
