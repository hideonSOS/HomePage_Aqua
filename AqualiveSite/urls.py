
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import indexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('top_page/', include('top_page.urls')),
    path('input_page/', include('input_page.urls')),
    path('room/', include('room.urls')),
    path('',indexView, name='indexview'),

]
