from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    Pro_User=models.OneToOneField(User,on_delete=models.CASCADE)
    Address=models.TextField()
    Pro_Pic=models.ImageField(upload_to='User')