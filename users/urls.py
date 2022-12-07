from django.urls import path
from . import views


urlpatterns = [
        path('signup/', views.SignUp.as_view(), name='signup'),
        path('login/', views.Login.as_view() , name = 'login'),
        path('writer/<int:pk>/', views.WritersPage.as_view() , name = 'writerspage'),
        path('writer/signup/', views.WriterSignUp.as_view(), name = 'writersignup'),
        path('update/<int:pk>', views.UserUpdateForm.as_view(), name = 'usersupdate'),
        path('update/writer/profile/<int:pk>', views.UpdateWriterProfile.as_view(), name = 'writerprofile'),
        path('activate/<uidb64>/<token>', views.activate, name='activate'),
]