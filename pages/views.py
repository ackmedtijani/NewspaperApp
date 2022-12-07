from ast import keyword
from django.shortcuts import render
from articles.models import *
from django.views.generic import TemplateView, ListView
from articles.models import Article
from django.contrib import messages


class HomePageView(TemplateView):
    template_name = 'home.html'
    model = Article

    # A collage for each type of the article except Headlines
    # Top two recent headlines are used in the first part of the page. 
    # Opinions in a 8 tweet grid. 
    # Advice in an 4 grid format

    def get_all_article_types(self):
        self.article_types = []
        for values in  self.model.objects.all().values('type').distinct():
            for key , value in values.items():
                self.article_types.append(value)

        return self.article_types
        

    def get_context_data(self, **kwargs):
        context = {'article': self.model}
        for i in self.get_all_article_types():
            context[i] = self.model.objects.filter(type=i)
        
        return context

    
    def get(self, request):
        context = self.get_context_data()
        if self.request.user.is_authenticated:
            context['writer'] = self.request.user.is_writer()
            context['reader'] = self.request.user.is_reader()
            messages.success(request, f'Dear <b></b>, please go to you email <b></b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
            return self.render_to_response(context)
            
        else:
            return self.render_to_response(context)


    
    
    #Filter all the types of articles. Look for 
    
   
        #Finding the unique items in the type column of Article Model
        #Iterating through them giving each of them a context in the box. 
        #Placing the newest of each type onto the context. 


class OpinionPageView(ListView):
    template_name = 'opinions.html'
    paginate_by = 10

    def get(self, request , **kwargs):
        self.object_list = Article.objects.filter(type = 'OPINION')
        print(self.object_list)
        context = self.get_context_data()
        return self.render_to_response(context)

        #Check if the kwarg has the specific type of article and render template based on that. Apart from that filter the article list based on that. 
        #Putting the most read article on the left side of the websites. 
    #Do the same as the Homepage View but with opinion page as the only unique item

class HeadlinesPageView(ListView):
    pass

    #Do the same as the Homepage View but with the  HeadlinesPageView as the only unique page.
# Create your views here.

#Or using the url string in the urlconf to determine the type of Article content to rendered
#For example a '/opinions' will render an opinion page and headlines will render an headline page.


