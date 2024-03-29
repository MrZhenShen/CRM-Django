from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Client(AbstractUser):
  telephone_number = models.CharField(max_length=15)
  company_name = models.CharField(max_length=30)
  company_link = models.CharField(max_length=50, default='-')
  industry = models.CharField(max_length=20)
  role = models.CharField(max_length=20, default='-')
  country = models.CharField(max_length=20, default='-')
  city = models.CharField(max_length=20, default='-')

class Good(models.Model):
  name = models.CharField(max_length=20)
  description = models.CharField(max_length=200)
  example_image = models.CharField(max_length=300)
  pricing = models.CharField(max_length=20)

class Status(models.Model):
  title = models.CharField(max_length=20)
  color = models.CharField(max_length=20)

class Project(models.Model):
  Good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True)
  Client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
  client_comment = models.CharField(max_length=300)
  Status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
