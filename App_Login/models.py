from django.db import models

# To Create A Custom User Model and admin panel
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import ugettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class MyuserManager(
    BaseUserManager
):  # To Manage new users using this baseusermanaegr class
    """ A Custom User Manager to deal with Emails  as an unique Identifier """

    def _create_user(self, email, username, password, **extra_fields):
        """Creates and Saves an user with given email and password """

        if not email:
            raise ValueError("Email Must Be Set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("SuperUser is_staff must be True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("SuperUser is_superuser must be True")

        return self._create_user(email, username, password, **extra_fields)


ROLES = (
        ('Employee', 'Employee'),
        ('Customer', 'Customer'),
        ('Admin', 'Admin'),
    )

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=264,unique=True)
    roles=models.CharField(max_length=40,choices=ROLES,default=ROLES[1][1])
    is_staff = models.BooleanField(
        ugettext_lazy("staff_status"),
        default=False,
        help_text="Determines Whether They Can Log in this Site or not",
    )
    is_active = models.BooleanField(
        ugettext_lazy("active"),
        default=True,
        help_text="Determines Whether their Account Status is Active or not",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = MyuserManager()

    class Meta:
        verbose_name_plural = "User"
        db_table = "User"

    def __str__(self):
        return self.email

def upload_image(instance, filename):
    return "profile/{instance.user.username}/{instance.user.username}profile_pic.png".format(instance=instance)



class Profile(models.Model):
    full_name = models.CharField(max_length=264, blank=True)
    profile_pic=models.ImageField(upload_to=upload_image,blank=True,default='/profile/avatar.jpg')    
    phone = models.CharField(max_length=20, blank=True)
    address=models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
    

    class Meta:
        verbose_name_plural = "Profile"
        db_table = "Profile"
        

class Customer(Profile):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile',)

    def __str__(self):
        return self.user.username+" 's Profile"

class AdminProfile(Profile):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='admin_profile',)

    def __str__(self):
        return self.user.username+" 's Profile"

    
    
class Staff(Profile):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='staff_profile',)
    staff_code=models.CharField(max_length=50,blank=True)
    is_verified=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username+" 's Profile"


        

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if instance.roles=='Employee':
        Staff.objects.get_or_create(user=instance,full_name=instance.username)
    elif instance.roles=='Admin' or instance.is_staff:
        AdminProfile.objects.get_or_create(user=instance,full_name=instance.username)
    else:
        Customer.objects.get_or_create(user=instance,full_name=instance.username)

@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
   if instance.roles=='Employee':
        instance.staff_profile.save()
   elif instance.roles=='Admin' or instance.is_staff:
        instance.admin_profile.save()
   else:
        instance.customer_profile.save()
   


