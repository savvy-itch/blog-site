from django.test import TestCase
from articles.forms import SubscribeForm

class SubscribeFormTest(TestCase):
  def test_email_field_label(self):
    form = SubscribeForm()
    self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Subscribe to the newsletter!')
  
  def test_subscribe_invalid_email(self):
    form = SubscribeForm(data={'email': 'invalid_email'})
    self.assertFalse(form.is_valid())
  
  def test_subscribe_valid_email(self):
    form = SubscribeForm(data={'email': 'valid@mail.com'})
    self.assertTrue(form.is_valid())