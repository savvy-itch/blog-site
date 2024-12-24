from django.shortcuts import render
from django.views import generic
from .models import Article, Tag

class ArticleListView(generic.ListView):
  model = Article
  template_name = 'index.html'


class ArticleDetailView(generic.DetailView):
  model = Article

class TagListView(generic.ListView):
  model = Tag
  template_name = 'base_generic.html'

def filtered_articles(request):
  filters = request.GET.getlist('tags')
  print(filters)
  if filters:
    articles = Article.objects.filter(tags__name__in=filters).distinct()
  else:
    articles = Article.objects.all()
  num_articles = articles.count()
  return render(request, 'index.html', {'articles': articles, 'num_articles': num_articles, 'filters': filters})
