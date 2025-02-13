import markdown
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.core.validators import MinLengthValidator

class Tag(models.Model):
  name = models.CharField(
    max_length=200,
    unique=True,
    help_text="Enter a new tag (e.g. React, browser extension, etc.)"
  )

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']
    constraints = [
      UniqueConstraint(
        Lower('name'),
        name='tag_name_case_insensitive_unique',
        violation_error_message = "Tag already exists (case insensitive match)"
      )
    ]

class Article(models.Model):
  title = models.CharField(max_length=200, unique=True)
  pub_date = models.DateField('date published')
  short_desc = models.TextField('short description', null=True, max_length=240, validators=[MinLengthValidator(3)])
  thumbnail = models.URLField('thumbnail', default='https://placehold.co/400x240')
  content = models.TextField(validators=[MinLengthValidator(2)])
  tags = models.ManyToManyField(Tag, help_text="Select tags for this article")

  def html_content(self):
    return markdown.markdown(self.content, extensions=['extra', 'fenced_code', 'codehilite'])
  
  def display_tags(self):
    return ', '.join(tag.name for tag in self.tags.all())
  
  display_tags.short_description = 'Tags'

  def get_absolute_url(self):
    return reverse('article-detail', args=[str(self.id)])

  def __str__(self):
    return self.title
  
  class Meta:
    ordering = ['-pub_date']

class SubscriberEmail(models.Model):
  email = models.EmailField(validators=[MinLengthValidator(6)], max_length=200, unique=True)

  def __str__(self):
    return self.email
