from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('opinions/', views.OpinionPageView.as_view(), name='opinion'),

]