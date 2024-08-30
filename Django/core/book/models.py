from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Emenitites(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Blog(models.Model):
	blog_name =models.CharField(max_length=100)
	blog_description = models.TextField()
	price = models.IntegerField()
	emenities = models.ManyToManyField(Emenitites)
	
	def __str__(self):
		return self.blog_name
