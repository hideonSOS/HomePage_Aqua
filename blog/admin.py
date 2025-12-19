
from django.contrib import admin
from django.utils.safestring import mark_safe
from input_page.models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # 管理画面の一覧に表示する項目
    list_display = ('preview', 'post_date', 'description_short')
    
    # 日付でフィルタリングできるようにする
    list_filter = ('post_date',)

    # 画像のプレビューを表示するメソッド
    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 100px; height: auto;">')
        return "画像なし"
    preview.short_description = 'プレビュー'

    # 説明文が長い場合に省略して表示
    def description_short(self, obj):
        if len(obj.description) > 30:
            return obj.description[:30] + "..."
        return obj.description
    description_short.short_description = '説明文'