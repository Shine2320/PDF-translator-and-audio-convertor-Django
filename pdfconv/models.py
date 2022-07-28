from fileinput import filename
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserPDF(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, blank=True, null=True)