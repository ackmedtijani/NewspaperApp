
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.forms import BooleanField, CharField, SlugField
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField



class CustomUser(AbstractUser):
    class Type(models.TextChoices):
        ADMIN = 'ADMIN', 'admin'
        WRITER='WRITER', 'writer'
        READER='READER', 'reader'

    type_choice = Type.READER

    username = models.CharField(max_length=255,blank=True, null=True, unique=False)
    first_name = models.CharField(max_length= 100, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, unique=True, null=True)
    middle_name = models.CharField(max_length=150 , blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(_('Type'), max_length=50, choices=Type.choices)
    slug = models.SlugField(max_length=264, unique=True, null=True)
    



    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password', 'type']
    USERNAME_FIELD = 'email'


    def get_full_name(self):
        if self.middle_name:
            return self.first_name + ' ' + self.middle_name + ' ' + self.last_name 
        else:
            return super().get_full_name()

    def get_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return "{}".format(self.email)

    def save(self, *args, **kwargs):
        if self.id:
            self.type = self.type_choice
        return super().save(*args , **kwargs)

    def is_writer(self):
        return True if self.type.lower() == 'writer' else False 

    def is_reader(self):
        return True if self.type.lower() == 'reader' else False



class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Type.ADMIN)


class Admin(CustomUser):

    type_choice = CustomUser.Type.ADMIN
    admin = AdminManager()

    class Meta:
        proxy = True

    def save(self ,*args , **kwargs):
        self.type = self.type_choice
        if self.type == 'ADMIN':   
            self.is_staff = True
            return super().save(*args , **kwargs)


class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    admin_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.user.email)


@receiver(post_save, sender=Admin)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.type == "ADMIN":
        AdminProfile.objects.create(user=instance)


class ReaderManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Type.READER)


class Reader(CustomUser):

    type_choice = CustomUser.Type.READER

    student = ReaderManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"

    def save(self, *args, **kwargs):
        self.type = self.type_choice
        return super().save(*args , **kwargs)


@receiver(post_save, sender=Reader)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.type == "READER":
        ReaderProfile.objects.create(user=instance)


class ReaderProfile(models.Model):
    user = models.OneToOneField(Reader, on_delete=models.CASCADE)
    reader_id = models.IntegerField(null=True, blank=True) 
    nationality = CountryField(null = True, blank_label = 'select country')

    def __str__(self):
        return "{}".format(self.user.email)



class WriterManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(type=CustomUser.Type.WRITER)


class Writer(CustomUser):

    type_choice = CustomUser.Type.WRITER

    writer = WriterManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for teachers"

    def save(self, *args, **kwargs):
        self.type = self.type_choice
        self.slug = slugify(self.get_name())
        return super().save(*args , **kwargs)

    def get_absolute_url(self):
        return reverse('writerspage', kwargs = {'pk' : str(self.id)})
      


class WriterProfile(models.Model):
    user = models.OneToOneField(Writer, on_delete=models.CASCADE)
    image = models.ImageField(default = '666201.png', blank= False, null = False,  upload_to = 'images/')
    bio = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=255 , null=True, blank=True)
    nationality = CountryField(null = True, blank_label = 'select country')

    def __str__(self):
        return "{}".format(self.user.email)

    def get_absolute_url(self):
        return reverse('writerspage' , kwargs= {'pk': self.user.id})


@receiver(post_save, sender=Writer)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.type == "WRITER":
        WriterProfile.objects.create(user=instance)




# Create your models here.
