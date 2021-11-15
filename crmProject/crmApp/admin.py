from django.contrib import admin

# Register your models here. 

# login: admin
# password: qwerty

from .models import Client, Good, Status, Project

admin.site.register(Client)
admin.site.register(Good)
admin.site.register(Status)
admin.site.register(Project)
