from django import forms
from . import models
from users.models import Writer

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('comment',)


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label="Title" , widget=forms.TextInput(attrs={'placeholder': 'Enter the title....'}))
    summary = forms.CharField(label='Summary' , widget=forms.TextInput(attrs={'placeholder': 'Brief summary of the article....'}))
    author = forms.ModelMultipleChoiceField(queryset= Writer.objects.filter(type = 'WRITER') , required = False)

    class Meta:
        model = models.Article
        fields = ['title', 'summary' , 'body',  'author' , 'image']

