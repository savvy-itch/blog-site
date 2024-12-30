from django.test import TestCase
from articles.models import Tag, Article

class TagModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Tag.objects.create(name='Python')
  
  def test_name_label(self):
    tag = Tag.objects.get(id=1)
    field_label = tag._meta.get_field('name').verbose_name
    self.assertEqual(field_label, 'name')

  def test_name_length(self):
    tag = Tag.objects.get(id=1)
    max_length = tag._meta.get_field('name').max_length
    self.assertEqual(max_length, 200)

class ArticleModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Article.objects.create(title='Test article', pub_date='2024-12-24')
  
  def test_title_label(self):
    article = Article.objects.get(id=1)
    field_label = article._meta.get_field('title').verbose_name
    self.assertEqual(field_label, 'title')

  def test_title_length(self):
    article = Article.objects.get(id=1)
    max_length = article._meta.get_field('title').max_length
    self.assertEqual(max_length, 200)
  
  def test_pub_date_label(self):
    article = Article.objects.get(id=1)
    field_label = article._meta.get_field('pub_date').verbose_name
    self.assertEqual(field_label, 'date published')

  def test_content_label(self):
    article = Article.objects.get(id=1)
    field_label = article._meta.get_field('content').verbose_name
    self.assertEqual(field_label, 'content')

  def test_tags_label(self):
    article = Article.objects.get(id=1)
    field_label = article._meta.get_field('tags').verbose_name
    self.assertEqual(field_label, 'tags')
  
  def test_get_absolute_url(self):
    article = Article.objects.get(id=1)
    self.assertEqual(article.get_absolute_url(), '/home/article/1/')
