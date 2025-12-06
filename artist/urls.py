from django.urls import path
from django.views.generic import TemplateView


app_name='artist'


urlpatterns=[
	path('',TemplateView.as_view(template_name='artist/artist.html'),name='artist')
]