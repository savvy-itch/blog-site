import json
from django.shortcuts import render
from django.views import generic
from .models import Article, Tag, SubscriberEmail
from django.core.paginator import Paginator
from articles.forms import SubscribeForm
from django.http import JsonResponse
from http import HTTPStatus

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
  
  mail_list = SubscriberEmail.objects.all()
  print(mail_list)
  # send_email_notification()
  
  return render(request, 'index.html', {
    'articles': articles, 
    'num_articles': num_articles, 
    'filters': filters, 
    'filters_url_params': filters_url_params, 
    'page_obj': page_obj
    })

def subscribe_to_email_notification(request):
  if request.method == 'POST':
    try:
      payload = json.loads(request.body)
      form = SubscribeForm(payload)

      if form.is_valid():
        form.save()
        return JsonResponse({'success_msg': 'Thank you for subscribing!'}, status=HTTPStatus.CREATED)
      else:
        return JsonResponse({'error_msg': form.errors.get('email', ['Invalid data'])[0]}, status=HTTPStatus.BAD_REQUEST)
    except json.JSONDecodeError:
      return JsonResponse({'error_msg': 'Invalid JSON payload'}, status=HTTPStatus.BAD_REQUEST)
    
  return JsonResponse({'error_msg': 'Invalid request method.'}, status=HTTPStatus.METHOD_NOT_ALLOWED)
