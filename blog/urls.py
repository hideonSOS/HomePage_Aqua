from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import blog_timeline

app_name='blog'

urlpatterns=[
	path('',blog_timeline,name='blog')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)