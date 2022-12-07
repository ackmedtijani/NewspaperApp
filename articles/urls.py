from random import vonmisesvariate
from django.urls import path
from . import views


urlpatterns = [
        path('create_new/', views.ArticleCreateView.as_view(), name='article_create'),
        path('<int:pk>/', views.articleDetail, name='article_detail'),
        path('update/page/<int:pk>/', views.ArticleUpdateView.as_view() , name='article_update'),
        path('delete/<int:pk>/', views.ArticleDeleteView.as_view() , name='article_delete'),
        path('comments/create', views.CommentCreateView.as_view(), name='comment_create'),
        #path('<int:pk>/comments/<int:pk>', views.CommentDetail, name = 'comment_detail'),
]