from django.db import models

# Create your models here.

class title(models.Model):
    title = models.CharField(max_length=20)#文章名
    address = models.CharField(max_length=20)#地址
