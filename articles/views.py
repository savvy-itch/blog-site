from django.shortcuts import render
from django.views import generic
from .models import Article, Tag
from django.core.paginator import Paginator

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
  paginator = Paginator(articles, 2)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  filters_url_params = ''
  for filter in filters:
    filters_url_params += f"&tags={filter}"
  print(filters_url_params)
  return render(request, 'index.html', {
    'articles': articles, 
    'num_articles': num_articles, 
    'filters': filters, 
    'filters_url_params': filters_url_params, 
    'page_obj': page_obj
    })
