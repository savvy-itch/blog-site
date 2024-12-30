import json
from django.test import TestCase
from articles.models import Tag, Article, SubscriberEmail
from django.urls import reverse
from http import HTTPStatus
from articles.email import send_email_notification
from django.core import mail

class FilteredArticlesTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    py_tag = Tag.objects.create(name='Python')
    js_tag = Tag.objects.create(name='JavaScript')
    article1 = Article.objects.create(title='Test article 1', pub_date='2024-12-24')
    article2 = Article.objects.create(title='Test article 2', pub_date='2024-11-24')
    article3 = Article.objects.create(title='Test article 3', pub_date='2024-11-25')
    article1.tags.set([py_tag])
    article2.tags.set([js_tag])
    article3.tags.set([js_tag])
  
  def test_view_url_exists_at_desired_location(self):
    response = self.client.get('/home/')
    self.assertEqual(response.status_code, 200)
  
  def test_view_url_accessible_by_name(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
  
  def test_view_url_uses_correct_template(self):
    response = self.client.get(reverse('index'))
    self.assertTemplateUsed(response, 'index.html')

  def test_all_displayed_articles(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['num_articles'], 3)

  def test_filtered_articles_displayed(self):
    response = self.client.get('/home/?tags=Python')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['num_articles'], 1)

  def test_all_articles_displayed_when_all_filters_checked(self):
    response = self.client.get('/home/?tags=Python&tags=JavaScript')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['num_articles'], 3)
  
  def test_pagination_is_two(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertTrue('page_obj' in response.context)
    self.assertTrue(response.context['page_obj'].has_other_pages())
    self.assertEqual(len(response.context['page_obj'].object_list), 2)
  
  def test_lists_all_articles(self):
    page = 2
    response = self.client.get(reverse('index') + f'?page={page}')
    self.assertEqual(response.status_code, 200)
    self.assertTrue('page_obj' in response.context)
    self.assertEqual(len(response.context['page_obj'].object_list), 1)

class TagListViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Tag.objects.create(name='Python')
    Tag.objects.create(name='JavaScript')

  def test_all_displayed_filters(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.context['tag_list']), 2)

  def test_applied_filters_displayed(self):
    response = self.client.get('/home/?tags=Python')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.context['filters']), 1)

class SubscribeToEmailNotification(TestCase):
  url = reverse('subscribe_to_email_notification')
  payload = json.dumps({'email': 'valid@mail.com'})
  headers = {'content_type': 'application/json'}

  def test_save_valid_email(self):
    response = self.client.post(self.url, self.payload, **self.headers)
    self.assertEqual(response.status_code, HTTPStatus.CREATED)
    success_msg = response.json()['success_msg']
    self.assertEqual(success_msg, 'Thank you for subscribing!')
  
  def test_reject_duplicate_email(self):
    response = self.client.post(self.url, self.payload, **self.headers)
    response = self.client.post(self.url, self.payload, **self.headers)
    self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
    error_msg = response.json()['error_msg']
    self.assertEqual(error_msg, 'Subscriber email with this Email already exists.')

  def test_send_email_when_new_article_published(self):
    recipient_email = SubscriberEmail.objects.create(email='test@mail.com')
    py_tag = Tag.objects.create(name='Python')
    article = Article.objects.create(title='Test article 1', pub_date='2024-12-24')
    article.tags.set([py_tag])

    send_email_notification(article.title, article.get_absolute_url, recipient_email)

    self.assertEqual(len(mail.outbox), 1)
    self.assertEqual(mail.outbox[0].subject, 'New article just published')
    self.assertEqual(mail.outbox[0].body, article.title)
