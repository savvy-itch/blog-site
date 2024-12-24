from .models import Tag

def tag_list_processor(request):
  return {"tag_list": Tag.objects.all()}