

# Create your models here.

from django.utils.text import slugify
from django.conf import settings
from django.db import models
from django.urls import reverse
from users.models import Writer
from ckeditor.fields import RichTextField

class Article(models.Model):

    class Type(models.TextChoices):
        OPINION = 'OPINION' , 'opinion'
        POLITICS = 'POLITICS', 'politics'
        HEADLINES = 'HEADLINES' , 'headlines'

    # prepopulating the slug fild

    #Add an image field for upload
        
    title = models.CharField(max_length= 255)
    slug = models.SlugField(blank=True, null=True, max_length=500)
    body = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    summary = models.CharField(max_length= 255)
    type = models.CharField('Type', max_length=255 , choices= Type.choices)
    image = models.ImageField(blank=True, null=True, upload_to = "articles/")
    author = models.ManyToManyField(Writer)
    created = models.DateTimeField(auto_now_add= True)

    #Write the help message of these articles in the Forms. 


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk' : self.id})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def list_author(self):
        if self.author.all():
           return list(self.author.all().values_list('email', flat=True))
        else: 
            return None

    @property
    def get_authors(self):
        return [author for author in self.author.all()]

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank = True, null=True, on_delete= models.CASCADE, related_name='parents')
    reply = models.ForeignKey('self', blank = True, null = True, on_delete= models.CASCADE , related_name= 'replies')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self): 
        return self.comment

    def get_absolute_url(self):
        return reverse('article_detail')
    
    @property
    def is_comment(self):
        if self.parent is None:
            return True
        return False

    @property
    def all_replies(self):
        if self.reply: 
            return Comment.objects.filter(parent = self)
        return None

    @property
    def has_reply(self):
        if self.reply is None:
            return False
        return True

   




    
