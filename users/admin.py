from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *
from .models import *

class ReaderUserAdmin(UserAdmin):
    add_form = ReaderCreationForm
    list_display = ['email',  'first_name' , 'last_name' , 'type']
    model = Reader

class WriterUserAdmin(UserAdmin):
    add_form = WriterCreationForm
    list_display = ['email', 'first_name' , 'last_name' , 'type']
    model = Writer

class AdminsUserAdmin(UserAdmin):
    add_form = AdminCreationForm
    list_display = ['email', 'first_name' , 'last_name' , 'type']
    model = Admin

class WriterProfileAdmin(admin.ModelAdmin):
    model = WriterProfile
    add_form = WriterProfileForm
    list_display = ['user', 'education']


admin.site.register(Reader, ReaderUserAdmin)
admin.site.register(Writer, WriterUserAdmin)
admin.site.register(Admin , AdminsUserAdmin)
admin.site.register(WriterProfile, WriterProfileAdmin)
admin.site.register(CustomUser)


# Register your models here. 
