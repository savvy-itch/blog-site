from django.urls import path, re_path
from . import views

urlpatterns = [
  path('', views.filtered_articles, name='index'),
  path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
  path('subscribe/', views.subscribe_to_email_notification, name='subscribe_to_email_notification')
]