from django import forms
from .models import SubscriberEmail
from django.utils.translation import gettext_lazy as _

class SubscribeForm(forms.ModelForm):
  class Meta:
    model = SubscriberEmail
    fields = ['email']
    labels = {'email': 'Subscribe to the newsletter!'}
    widgets = {'email': forms.EmailInput(attrs={
      'placeholder': 'example@mail.com',
    })}
