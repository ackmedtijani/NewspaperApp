from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import DetailView , ListView , TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse , HttpResponseRedirect
from .form import CommentForm , ArticleForm

# Create your views here.

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    raise_exception = False

    def test_func(self):
        type = self.request.user.type.lower()
        return type.endswith('writer')
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            if self.request.user not in form.instance.author.all():
                form.instance.author.add(Writer.objects.get(id = self.request.user.id))
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.form_invalid(form)


class ArcDetailView(LoginRequiredMixin, TemplateView):
    model = Article
    login_url = 'login'
    
    def get(self, request, *args,  **kwargs):
            pk = kwargs.get('pk')
            self.object = self.model.objects.get(id = pk)
            context = self.get_context_data()
            return super().get(request, *args, **kwargs)



def articleDetail(request, *args , **kwargs):
    pk = kwargs.get('pk')
    object = Article.objects.get(id = pk)
    comments = Comment.objects.filter(article = object)


    def check_article(list , object):
        if not object in list:
            list.append(object)

    if request.method == 'GET':
        form = CommentForm()
        try:
            articles_read = request.session['articles_read']
            print("Existing articles" , articles_read)
        except:
            request.session['articles_read'] = []
            articles_read = request.session['articles_read']
            print("New Sessions articles read", articles_read)
         
        if request.user.is_authenticated:
            check_article(articles_read , object.id)
        else:
            if len(articles_read) > 3:
                return HttpResponseRedirect('login')
            check_article(articles_read, object.id)
        print(articles_read)

        request.session.modified = True
        
        return render(request, 'articles/article_detail.html' , {'form': form , 'object': object, 'comments': comments})
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.article = object
        form.instance.author = request.user
        if form.is_valid():
            form.save()

        return redirect('article_detail' , pk = pk)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'articles/comment_create.html'
    fields = ['comment']
    raise_exception = False

    def get(self, request, *args, **kwargs):
        self.prev_url = self.request.META.get('HTTP_REFERER')
        import re
        if self.prev_url:
            if "comments" in self.prev_url:
                result = re.search("articles/(/d+)/comments/(/d+)", self.prev_url)
                comment_id , article_id = result.group(2) , result.group(1)
                self.article = Article.objects.get(id = article_id)
                self.comments = Comment.objects.get(id = comment_id)
            else:
                result = re.search("articles/(\d+)" , self.prev_url)
                result = result.group(1)
                self.article = Article.objects.get(id = result)
        return super().get(request, *args, **kwargs) 

    def form_valid(self, form): 
        print(self.request.user)
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            form.instance.author = self.request.user 
            if self.parent:
                form.instance.parent = self.parent
            form.instance.article = self.article
            return JsonResponse({"success":True}, status=200)

        return JsonResponse({"success":False}, status=400)

    
    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and self.request.POST.get('comment'):
            print(self.request.user)
            print(self.request.POST)
            comment = Comment.objects.get(id = self.request.POST.get('link'))
            if comment:
                self.parent = comment
                self.article = comment.article
            replies = Comment.objects.create(article = self.article, comment = self.request.POST.get('comment'), 
                author = self.request.user, parent = self.parent)
            comment.reply = replies
            comment.save()
            return JsonResponse({"success":True}, status=200)
                
        return super().post(request, *args, **kwargs)


    


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    login_url = 'login'
    #Add permission mixin to it. 

    def get(self, request, *args,  **kwargs):
        pk = kwargs.get(self.pk_url_kwarg)
        self.object = self.model.objects.get(id = pk)
        context = self.get_context_data()
        return super().get(request, *args, **kwargs)





class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'body', 'summary',  'image']
    template_name = 'articles/article_update.html'
    login_url = 'login'


    def test_func(self):
        def func():
            type = self.request.user.type.lower()
            #Check if the user has the same id as the user who created it
            pk = self.kwargs.get(self.pk_url_kwarg)
            articles = Article.objects.get(id = pk)
            if (self.request.user == articles.author) or self.request.user.type.lower().endswith('admin'):
                return True
            else:
                return False

        return func()

    
class ArticleDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Article
    template_engine = 'articles/article_delete.html'

    def test_func(self):
        def func():
            type = self.request.user.type.lower()
            #Check if the user has the same id as the user who created it
            pk = self.kwargs.get(self.pk_url_kwarg)
            articles = Article.objects.get(id = pk)
            if (self.request.user == articles.author) or self.request.user.type.lower().endswith('admin'):
                return True
            else:
                return False

        return func()