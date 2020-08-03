from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.
class UserProfileManager(BaseUserManager):
    """helps django to work with our custom user model"""
    def create_user(self, email, name, password=None):
        """create new user profile obj"""
        if not email:
            raise ValueError("Users must have a email")

        email=self.normalize_email(email)
        user=self.model(email=email,name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user


  def create_superuser(self,emial,name,password):
      user=self.crete_user(email,name,password)
      user.is_superuser = True
      user.is_staff = True
      user.save(using=self._db)

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Represents use profile inside our sys"""
    email = models.email(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    objects=UserProfileManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']
    def get_full_name(self):
        return self.name
        """used to get a users full name"""

   def get_full_name(self):
       return self.name


   def get_short_name(self):
       return self.name

  def __str__(self):
      """convert obj to str"""
      return self.email
