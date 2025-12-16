from django.contrib import admin
from .models import Schedule, SlideImage

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day','title','time','artist1','artist2','artist3','artist4')


@admin.register(SlideImage)
class SlideImageAdmin(admin.ModelAdmin):
    # 一覧画面で表示する項目
    list_display = ('id', 'order', 'image')
    # クリックして編集画面に入れる項目
    list_display_links = ('id',)
    # 一覧画面のまま編集できる項目（順序の入れ替えに便利）
    list_editable = ('order',)