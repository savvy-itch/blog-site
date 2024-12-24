from django.urls import path, re_path
from . import views

urlpatterns = [
  # path('', views.ArticleListView.as_view(), name='index'),
  path('', views.filtered_articles, name='index'),
  path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
]