from django.core.mail import send_mail
from .models import SubscriberEmail
from smtplib import SMTPException
from django.template.loader import render_to_string

def send_email_notification(title, link, to_email=None):
  subject = 'New article just published'
  html_content = render_to_string('email/email.html', {'title': title, 'link': link})
  text_content = title
  mail_list = [to_email] if to_email else list(SubscriberEmail.objects.values_list('email', flat=True))

  try:
    send_mail(subject, text_content, None, mail_list, html_message=html_content)
  except SMTPException as e:
    print(f"Failed to send email: {e}")
  except Exception as e:
    print(f"Unexpected error: {e}")
