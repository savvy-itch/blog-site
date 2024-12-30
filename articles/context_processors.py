from .models import Tag
from .forms import SubscribeForm

def tag_list_processor(request):
  return {"tag_list": Tag.objects.all()}

def subscribe_form_processor(request):
  return {'email_form': SubscribeForm()}