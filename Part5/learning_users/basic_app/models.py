from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    # Add more attributes to the user:
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional classes:
    portfolio_site = models.URLField(blank=True) #User does not have to fill it out.
    profile_pics = models.ImageField(upload_to = 'profile_pics', blank=True) #Profile_pics must be sub direcotory in media folder.

    def __str__(self):
        return self.user.username # username is default attribute of User.
