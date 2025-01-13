import json
from django.shortcuts import render
from django.views import generic
from .models import Article, Tag, SubscriberEmail
from django.core.paginator import Paginator
from articles.forms import SubscribeForm
from django.http import JsonResponse
from http import HTTPStatus
from django.core.signing import TimestampSigner, SignatureExpired
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

class ArticleDetailView(generic.DetailView):
  model = Article

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    current_article = self.object
    similar_articles = []

    current_tags = current_article.tags.values_list('id', flat=True)

    similar_articles = (
      # get articles with any of the same tags
      Article.objects.filter(tags__in=current_tags)
      .exclude(id=current_article.id)
      # count how many matching tags articles have
      .annotate(tag_count=Count('tags', filter=Q(tags__in=current_tags)))
      .order_by('-tag_count')[:2]
    )

    context["similar_articles"] = similar_articles
    return context

class TagListView(generic.ListView):
  model = Tag
  template_name = 'base_with_sidebar.html'

def filtered_articles(request):
  filters = request.GET.getlist('tags')
  print(filters)
  if filters:
    articles = Article.objects.filter(tags__name__in=filters).distinct()
  else:
    articles = Article.objects.all()
  num_articles = articles.count()
  paginator = Paginator(articles, 6)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  filters_url_params = ''
  for filter in filters:
    filters_url_params += f"&tags={filter}"
  
  return render(request, 'index.html', {
    'articles': articles, 
    'num_articles': num_articles, 
    'filters': filters, 
    'filters_url_params': filters_url_params,
    'page_obj': page_obj,
    'display_invisible_next_pages': page_obj.number < page_obj.paginator.num_pages - 2
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

def unsubscribe_from_notifications(request, token):
  try:
    decoded_email = TimestampSigner().unsign(token, max_age=60*60*24*3) # 3 days
  except SignatureExpired:
    return render(request, 'unsubscribe/index.html', {'error_msg': 'Unsubscribe link has been expired.', 'status_code': HTTPStatus.BAD_REQUEST}, status=HTTPStatus.BAD_REQUEST) # 400

  try:
    found_email = get_object_or_404(SubscriberEmail, email=decoded_email)
    found_email.delete()
    return render(request, 'unsubscribe/index.html', {'success_msg': 'You have successfully unsubscribed.'})
  except Exception:
    return render(request, 'unsubscribe/index.html', {'error_msg': 'Email not found.', 'status_code': HTTPStatus.BAD_REQUEST}, status=HTTPStatus.BAD_REQUEST) # 400


def about(request):
  return render(request, 'about/index.html')
