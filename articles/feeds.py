from django.contrib.syndication.views import Feed
from .models import Article
import environ

env = environ.Env(DEBUG=(bool, False))

class LatestEntriesFeed(Feed):
  title = "Michael Savych Blog"
  link = env("HOME_URL", default="http://127.0.0.1:8000/home/")
  description = "Programming articles, random thoughts and everything in-between"

  def items(self):
    return Article.objects.order_by("-pub_date")[:5]
  
  def item_title(self, item):
    return item.title
  
  def item_description(self, item):
    return item.short_desc