from django.contrib import admin
from .models import Article, Tag, SubscriberEmail
from .email import send_email_notification

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_display = ('title', 'pub_date', 'display_tags')
  list_filter = ('tags',)

  def save_model(self, request, obj, form, change):
    if not change:
      super().save_model(request, obj, form, change)
      send_email_notification(obj.title, obj.get_absolute_url)

admin.site.register(Tag)
admin.site.register(SubscriberEmail)