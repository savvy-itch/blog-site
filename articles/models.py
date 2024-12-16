import markdown
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.core.validators import MinLengthValidator, MinValueValidator

class Tag(models.Model):
  name = models.CharField(
    max_length=200,
    unique=True,
    help_text="Enter a new tag (e.g. React, browser extension, etc.)"
  )

  def __str__(self):
    return self.name

  class Meta:
    constraints = [
      UniqueConstraint(
        Lower('name'),
        name='tag_name_case_insensitive_unique',
        violation_error_message = "Tag already exists (case insensitive match)"
      )
    ]

class Article(models.Model):
  title = models.CharField(max_length=200)
  pub_date = models.DateField('date published')
  content = models.TextField(validators=[MinLengthValidator(2)])
  tags = models.ManyToManyField(Tag, help_text="Select tags for this article")

  def html_content(self):
    return markdown.markdown(self.content, extensions=['extra', 'fenced_code'])

  def get_absolute_url(self):
    return reverse('article-detail', args=[str(self.id)])

  def __str__(self):
    return self.title