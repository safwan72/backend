from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.DayTime)
admin.site.register(models.DishModel)
admin.site.register(models.AddOns)
admin.site.register(models.Variants)