
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import indexView
from django.conf import settings              # 追加
from django.conf.urls.static import static    # 追加

urlpatterns = [
    path('admin/', admin.site.urls),
    path('top_page/', include('top_page.urls')),
    path('input_page/', include('input_page.urls')),
    path('room/', include('room.urls')),
    path('history/', include('history.urls')),
    path('artist/', include('artist.urls')),
    path('blog/',include('blog.urls')),
    path('',indexView, name='indexview'),

]


# ↓↓↓ このブロックを追加 ↓↓↓
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)