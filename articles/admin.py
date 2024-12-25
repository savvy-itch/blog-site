from django.contrib import admin
from .models import Article, Tag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_display = ('title', 'pub_date', 'display_tags')
  list_filter = ('tags',)

admin.site.register(Tag)