import json
from django.test import TestCase
from articles.models import Tag, Article, SubscriberEmail
from django.urls import reverse
from http import HTTPStatus
from articles.email import send_email_notification
from django.core import mail
from articles.email import create_unsubscribe_link
from datetime import timedelta
from freezegun import freeze_time
from django.contrib.auth import get_user_model

class GetContextDataTest(TestCase):
  def test_display_similar_articles(self):
    js_tag = Tag.objects.create(name='JavaScript')
    article1 = Article.objects.create(title='Test article 1', pub_date='2024-12-24')
    article2 = Article.objects.create(title='Test article 2', pub_date='2024-11-24')
    article1.tags.set([js_tag])
    article2.tags.set([js_tag])
    response = self.client.get(f'/home/article/{article1.pk}/')
    self.assertEqual(response.context['similar_articles'][0], article2)
  
  def test_users_cannot_edit_articles(self):
    article = Article.objects.create(title='Test article 1', pub_date='2024-12-24')
    response = self.client.get(f'/home/article/{article.pk}/')
    self.assertNotContains(response, f'<a href="/admin/articles/article/{article.pk}/change/" target="_blank">Edit Article</a>', html=True)
  
  def test_admin_can_edit_articles(self):
    test_admin = get_user_model().objects.create_superuser(username='testadmin', password='1X<ISRUkw+tuK')
    article = Article.objects.create(title='Test article 1', pub_date='2024-12-24')

    self.client.login(username='testadmin', password='1X<ISRUkw+tuK')

    response = self.client.get(f'/home/article/{article.pk}/')
    self.assertContains(response, f'<a href="/admin/articles/article/{article.pk}/change/" target="_blank">Edit Article</a>', html=True)

class FilteredArticlesTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    py_tag = Tag.objects.create(name='Python')
    js_tag = Tag.objects.create(name='JavaScript')
    cpp_tag = Tag.objects.create(name='C++')
    cs_tag = Tag.objects.create(name='C#')
    article1 = Article.objects.create(title='Test article 1', pub_date='2024-12-24')
    article2 = Article.objects.create(title='Test article 2', pub_date='2024-11-24')
    article3 = Article.objects.create(title='Test article 3', pub_date='2024-11-25')
    article4 = Article.objects.create(title='Test article 4', pub_date='2025-01-09')

    article5 = Article.objects.create(title='Test article 5', pub_date='2025-02-11')
    article6 = Article.objects.create(title='Test article 6', pub_date='2025-02-12')
    article7 = Article.objects.create(title='Test article 7', pub_date='2025-02-13')

    article1.tags.set([py_tag])
    article2.tags.set([js_tag])
    article3.tags.set([js_tag])
    article4.tags.set([cpp_tag, cs_tag])

    article5.tags.set([py_tag])
    article6.tags.set([js_tag])
    article7.tags.set([js_tag])
  
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
    self.assertEqual(response.context['num_articles'], 7)

  def test_filtered_articles_displayed(self):
    response = self.client.get('/home/?tags=Python')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['num_articles'], 2)

  def test_all_articles_displayed_when_multiple_filters_checked(self):
    response = self.client.get('/home/?tags=Python&tags=JavaScript')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['num_articles'], 6)
  
  def test_pagination_is_two(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertTrue('page_obj' in response.context)
    self.assertTrue(response.context['page_obj'].has_other_pages()) # change items to 2 in filtered_articles for this test
    self.assertEqual(len(response.context['page_obj'].object_list), 6)
  
  def test_lists_all_articles(self):
    page = 2
    response = self.client.get(reverse('index') + f'?page={page}')
    self.assertEqual(response.status_code, 200)
    self.assertTrue('page_obj' in response.context)
    self.assertEqual(len(response.context['page_obj'].object_list), 1)
  
  def test_filtered_articles_with_special_symbols_in_tags(self):
    response = self.client.get('/home/?tags=C%2B%2B&tags=C%23')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['num_articles'], 1)

class TagListViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Tag.objects.create(name='Python')
    Tag.objects.create(name='JavaScript')
    Tag.objects.create(name='C#')

  def test_all_displayed_filters(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.context['tag_list']), 3)

  def test_applied_filters_displayed(self):
    response = self.client.get('/home/?tags=Python')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.context['filters']), 1)
  
  def test_tags_with_special_symbols_encoded_correctly(self):
    response = self.client.get('/home/?tags=C%23')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['filters'][0], 'C#')

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

class UnsubscribeFromNotifications(TestCase):
  def test_unsubscribe_with_valid_token(self):
    recipient_email = SubscriberEmail.objects.create(email='test@mail.com')
    unsubscribe_link = f'{create_unsubscribe_link(recipient_email)}'
    response = self.client.get(unsubscribe_link)
    self.assertEqual(response.status_code, 200)
    self.assertFalse(SubscriberEmail.objects.filter(email='test@mail.com').exists())
    self.assertEqual(response.context['success_msg'], 'You have successfully unsubscribed.')
  
  def test_unsubscribe_with_expired_token(self):
    recipient_email = SubscriberEmail.objects.create(email='test@mail.com')
    unsubscribe_link = f'{create_unsubscribe_link(recipient_email)}'
    
    with freeze_time() as frozen_time:
      frozen_time.tick(delta=timedelta(days=3, seconds=1))

      response = self.client.get(unsubscribe_link)
      self.assertEqual(response.status_code, 400)
      self.assertTrue(SubscriberEmail.objects.filter(email='test@mail.com').exists())
      self.assertEqual(response.context['error_msg'], 'Unsubscribe link has been expired.')

  def test_unsubscribe_invalid_email(self):
    unsubscribe_link = f'{create_unsubscribe_link('invalid@mail.com')}'
    response = self.client.get(unsubscribe_link)
    self.assertEqual(response.status_code, 400)
    self.assertFalse(SubscriberEmail.objects.filter(email='invalid@mail.com').exists())
    self.assertEqual(response.context['error_msg'], 'Email not found.')
