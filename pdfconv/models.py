from fileinput import filename
from PyPDF2 import PdfFileMerger
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserPDF(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255,null=True) 
    pdffile = models.FileField(upload_to='pdf/', blank=True, null=True)
class UserAudio(models.Model):
    pdf = models.ForeignKey(UserPDF,on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, blank=True)
