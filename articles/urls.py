from django.urls import path
from . import views
from .feeds import LatestEntriesFeed

urlpatterns = [
  path('', views.filtered_articles, name='index'),
  path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
  path('subscribe/', views.subscribe_to_email_notification, name='subscribe_to_email_notification'),
  path('unsubscribe/<str:token>', views.unsubscribe_from_notifications, name='unsubscribe_from_notifications'),
  path('about/', views.about, name='about'),
  path('reading_list/', views.reading_list, name='reading_list'),
  path('latest/feed/', LatestEntriesFeed(), name='rss'),
  path('articles/', views.get_articles, name='articles')
]