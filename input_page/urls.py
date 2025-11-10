from django.urls import path
from django.views.generic import TemplateView
from .views import ScheduleShow, ScheduleCreateView,ScheduleListView,ScheduleDeleteView,ScheduleUpdateView
from django.contrib.auth import views as auth_views

app_name = 'input_page'


urlpatterns = [
	path('', ScheduleShow.as_view(), name='input_page'),
    path('input/', ScheduleCreateView.as_view(), name='input'),
    path('list/', ScheduleListView.as_view(), name='list'),
    path('delete/<int:pk>/', ScheduleDeleteView.as_view(), name='delete'),
    path('update/', ScheduleUpdateView.as_view(), name='update'),
    path('login/', auth_views.LoginView.as_view(),name='login'),
    path('artist/', TemplateView.as_view(template_name='input_page/artist.html'), name='artist'),
    path('history/', TemplateView.as_view(template_name='input_page/history.html'), name='history')
]