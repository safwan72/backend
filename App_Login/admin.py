from django.contrib import admin
from . import models


# Register your models here.


admin.site.register(models.User)
admin.site.register(models.Staff)
admin.site.register(models.Customer)
admin.site.register(models.AdminProfile)

