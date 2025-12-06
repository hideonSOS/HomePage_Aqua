from django.db import models


class Schedule(models.Model):
    day = models.DateField()
    title = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    artist = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.day} - {self.title} - {self.time} - {self.artist}"


class SlideImage(models.Model):
    
    # 画像ファイルの実体は 'media/slides/' フォルダに保存されます
    image = models.ImageField("スライド画像", upload_to='slides/')
    
    # 表示順を制御するためのフィールド
    order = models.IntegerField("表示順", default=0, help_text="小さい数字ほど先に表示されます")

    class Meta:
        ordering = ['order'] # デフォルトで order 順に並ぶように設定

    def __str__(self):
        return f"スライド画像 {self.id}"