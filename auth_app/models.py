from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'profile' )


