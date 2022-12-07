from django.contrib import admin
from django.forms import ModelForm
from . import models

class ArticleForm(ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'body' , 'summary',  'author']

class CommentInline(admin.TabularInline):
    model = models.Comment


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    list_display = ('title' , 'list_author', 'type' , 'slug' , 'created' , 'image')
    list_filter = ('type', 'author')
    inlines = [CommentInline]

   
    

admin.site.register(models.Article , ArticleAdmin)
admin.site.register(models.Comment)



