from django.core.mail import send_mail
from .models import SubscriberEmail
from smtplib import SMTPException
from django.template.loader import render_to_string
from django.core.signing import TimestampSigner
from django.urls import reverse

def send_email_notification(title, link, to_email=None):
  subject = 'New article just published'
  text_content = title
  mail_list = [to_email] if to_email else list(SubscriberEmail.objects.values_list('email', flat=True))
  
  for email in mail_list:
    base_url = f"http://127.0.0.1:8000/"
    unsubscribe_link = f'{base_url}{create_unsubscribe_link(email)}'
    html_content = render_to_string('email/email.html', {'title': title, 'link': link, 'unsubscribe_link': unsubscribe_link})

    try:
      send_mail(subject, text_content, None, [email], html_message=html_content)
    except SMTPException as e:
      print(f"Failed to send email: {e}")
    except Exception as e:
      print(f"Unexpected error: {e}")

def create_unsubscribe_link(email):
  token = create_token(email)
  return reverse('unsubscribe_from_notifications', kwargs={'token': token})

def create_token(email):
  return TimestampSigner().sign(email)
