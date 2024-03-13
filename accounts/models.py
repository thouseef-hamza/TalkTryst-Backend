from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from core.generate import generate_otp,generate_username

class MyAccountManager(BaseUserManager):
    def create_user(self, full_name,phone_number,otp):
        if not phone_number:
            raise ValueError("User Must Have An Phone Number")

        user = self.model(
            full_name=full_name,
            phone_number=phone_number,
            otp=otp
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone_number):
        user = self.create_user(
            full_name=full_name,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    full_name = models.CharField(max_length=150)
    phone_number=models.CharField(max_length=15,unique=True)
    otp=models.CharField(max_length=7,default=generate_otp)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.full_name

    # if the superuser, he has the permission to change
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class Profile(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE,related_name="user_profile")
    username=models.CharField(max_length=30,unique=True)
    profile_picture=models.ImageField(upload_to="profile/",default="profile/default.png")
    email=models.EmailField(max_length=100,null=True,unique=True)
    
    def __str__(self) -> str:
        return self.user.full_name + " " + self.username
    
    