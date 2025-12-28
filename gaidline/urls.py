from django.urls import path
from django.views.generic import TemplateView

app_name = 'gaidline'

urlpatterns=[
	path('',TemplateView.as_view(template_name='gaidline/gaidline.html'),name='gaidline'),
]