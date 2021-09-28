from django.db import models
from decimal import Decimal
# Create your models here.
def upload_category(instance, filename):
    return "Category/{instance.name}/{instance.name}.png".format(instance=instance)

class Category(models.Model):
    name=models.CharField(max_length=150)
    picture=models.ImageField(upload_to=upload_category,blank=True,null=True)
    isActive=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name    
    class Meta:
        verbose_name_plural = "Category"
        db_table = "Category"
        
class DayTime(models.Model):
    name=models.CharField(max_length=150)
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name    
    
    class Meta:
        verbose_name_plural = "DayTime"
        db_table = "DayTime"
       
        
def upload_image(instance, filename):
    return "Dish/{instance.dish_name}/{instance.dish_name}.png".format(instance=instance)

class AddOns(models.Model):
    name=models.CharField(max_length=150)
    price=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name    
    
    class Meta:
        verbose_name_plural = "AddOns"
        db_table = "AddOns"

class Variants(models.Model):
    variant_name=models.CharField(max_length=30)
    price=models.IntegerField(default=0)
    added_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return self.variant_name    
    
    class Meta:
        verbose_name_plural = "Variants"
        db_table = "Variants"

    
        
def upload_image(instance, filename):
    return "Dish/{instance.dish_name}/{instance.dish_name}.png".format(instance=instance)


class DishModel(models.Model):
    dish_name=models.CharField(max_length=150)
    dish_picture=models.ImageField(upload_to=upload_image,blank=True,null=True)
    dish_category=models.ManyToManyField(Category,blank=True)
    dish_daytime=models.ManyToManyField(DayTime,blank=True)
    dish_description=models.TextField(blank=True)
    price=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
    dish_vat=models.IntegerField(default=0)
    dish_tax=models.IntegerField(default=0)
    added_at=models.DateTimeField(auto_now_add=True)
    availability=models.BooleanField(default=False)
    featured=models.BooleanField(default=False)

    @property
    def new_price(self):
        price=self.price+(self.price*((self.dish_vat)/100))+(self.price*((self.dish_tax)/100))
        return round(Decimal(price-(price*((self.discount)/100))),3) 
    

    def __str__(self):
        return self.dish_name

    class Meta:
        verbose_name_plural = "Dish"
        db_table = "Dish"
        
        