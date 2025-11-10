from django.urls import path
from django.views.generic import TemplateView

app_name='room'

urlpatterns = [
	path('', TemplateView.as_view(template_name='room/room.html'), name='room')
]