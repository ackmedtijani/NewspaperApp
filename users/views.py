from turtle import update
from django.shortcuts import render, redirect , get_object_or_404
from django.template.loader import render_to_string
from users.models import *
from articles.models import Article
from django.urls import reverse_lazy , reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import *
from django.conf import settings
from django.http import Http404,   HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate , login, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage , send_mail
from .tokens import account_activation_token

#Creating a LoginForm Class

def user_not_authenticated(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator


def activateEmail(request, user, to_email):
    mail_subject ='Activate your account'
    user = get_object_or_404(CustomUser , email = user)
    token = account_activation_token.make_token(user)
    message = render_to_string('users/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject,  message,  to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('home')



class SignUp(generic.CreateView):
    form_class = ReaderCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    
    def get(self, request ,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            print(self.request.user)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        print(user)
        print("POST REQUEST" , self.request.POST)
        user = user.email
        activateEmail(self.request, user, form.cleaned_data['email'])
        return HttpResponseRedirect(self.success_url)
    

class Login(LoginView):

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email = email, password = password)

        if user.is_authenticated:
            customuser = CustomUser.objects.get(email = email)
            if customuser.type.lower() == 'writer':
                login(self.request , user)
                self.success_url = reverse('writerspage', kwargs= {'pk': user.id})
                return HttpResponseRedirect(self.success_url)
            elif customuser.type.lower() == 'reader':
                login(self.request , user)
                self.success_url = reverse('home')
                return HttpResponseRedirect(self.success_url)


#Overriding the login in view can creating a login

class WriterSignUp(generic.CreateView):
    model = Writer
    form_class = WriterCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration\writer-signup.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(self.request, user, form.cleaned_data['email'])
            return HttpResponseRedirect(self.success_url)
        else:
            for error in list(form.errors.values):
                messages.error(self.request, error)

class WritersPage(generic.DetailView):

    model = Writer
    template_name = 'users/writerspage.html'

    #List of articles by the user

    #Using the slug or pk to find a list of articles written by the user.

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = Writer.objects.get(id=kwargs.get(self.pk_url_kwarg))
        context = self.get_context_data()
        context['writerbio'] = self.get_writer_bio(self.object)
        articles = Article.objects.filter(author = self.object)
        print(self.request.META.get('HTTP_REFERER'))
        if articles != None:
            context['articles'] = articles
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        context = {}
        if self.object:
            context['object'] = self.object
        context.update(kwargs)
        return context


    def get_writer_bio(self, user):
        writerprofile = WriterProfile.objects.get(user = user)
        return writerprofile


class UserUpdateForm(generic.UpdateView):

    fields = ['first_name' , 'last_name' , 'middle_name' ]
    template_name = 'users/usersupdate.html'


    def test_func(self , **kwargs):
        if self.request.user.id != kwargs.get('pk'):
            return HttpResponseRedirect('home')


    def get(self, request, *args , **kwargs):
        if self.request.user.is_authenticated:
            self.writersbio = None
            self.test_func(**kwargs)
            if self.request.user.type.lower() == 'writer':
                self.model= Writer
                self.object = Writer.objects.get(id = kwargs.get('pk'))
                self.writersbio = WriterProfile.objects.get(user = self.object) 
            else:
                self.model = CustomUser
                self.object = CustomUser.objects.get(id = kwargs.get('pk'))
            context = self.get_context_data()
            if self.writersbio is not None:
                context['writersbio'] = self.writersbio
                print(self.writersbio.id)
            return self.render_to_response(context)
        else:
            return HttpResponseRedirect('login')
        
    def get_success_url(self):
        if self.get_context_object_name(self.object).lower() == 'writer':
            return redirect('writerprofile', kwargs={'pk': self.writersbio.id})
        else:
            return reverse('home')

    def post(self, request, *args , **kwargs):
        if self.request.user.type.lower() == 'writer':
            self.model= Writer
            self.object = Writer.objects.get(id = kwargs.get('pk'))
            self.writersbio = WriterProfile.objects.get(user = self.object)
        else:
            self.model = CustomUser
            self.object = CustomUser.objects.get(id = kwargs.get('pk'))
        print(self.object)
        return super().post(request, *args, **kwargs)

class UpdateWriterProfile(generic.UpdateView):
    model = WriterProfile
    fields = ['image', 'bio' , 'education' , 'nationality']
    template_name = 'users/writerprofile.html'




        
        

        


                
            

    #Fitter out articles based on the writer's ID. 

    


