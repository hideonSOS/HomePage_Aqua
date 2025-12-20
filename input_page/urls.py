from django.urls import path
from django.views.generic import TemplateView
from .views import ScheduleShow, ScheduleCreateView,ScheduleListView,ScheduleDeleteView,ScheduleUpdateView
from django.contrib.auth import views as auth_views
from .views import blog_input, blog_list, blog_delete, blog_update

app_name = 'input_page'

urlpatterns = [
	path('', ScheduleShow.as_view(), name='input_page'),
    path('input/', ScheduleCreateView.as_view(), name='input'),
    path('list/', ScheduleListView.as_view(), name='list'),
    path('delete/<int:pk>/', ScheduleDeleteView.as_view(), name='delete'),
    path('update/', ScheduleUpdateView.as_view(), name='update'),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('blog/list/', blog_list, name='blog_list'),
    path('blog/input/', blog_input, name='blog_input'),
    path('blog/update/<int:pk>/', blog_update, name='blog_update'),
    path('blog/delete/<int:pk>/', blog_delete, name='blog_delete'),
]

