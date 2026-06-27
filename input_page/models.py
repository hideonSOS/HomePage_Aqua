from django.db import models
from django.utils import timezone

class Schedule(models.Model):
    day = models.DateField()
    title = models.CharField(max_length=30, blank=True, default='')
    time = models.CharField(max_length=30, blank=True, default='')
    seminar = models.BooleanField(default=False)
    artist1 = models.CharField(max_length=50, null=True, blank=True)
    artist2 = models.CharField(max_length=50, null=True, blank=True)
    artist3 = models.CharField(max_length=50, null=True, blank=True)
    artist4 = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return f"{self.day} - {self.title} - {self.time} - {self.artist1}- {self.artist2}- {self.artist3}- {self.artist4}"





class SlideImage(models.Model):
    
    # 画像ファイルの実体は 'media/slides/' フォルダに保存されます
    image = models.ImageField("スライド画像", upload_to='slides/')
    
    # 表示順を制御するためのフィールド
    order = models.IntegerField("表示順", default=0, help_text="小さい数字ほど先に表示されます")

    class Meta:
        ordering = ['order'] # デフォルトで order 順に並ぶように設定

    def __str__(self):
        return f"スライド画像 {self.id}"

class AccessLog(models.Model):
    page = models.CharField(max_length=255)
    accessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "アクセスログ"


class YouTubeLive(models.Model):
    video_id   = models.CharField("YouTube Video ID", max_length=20,
                                  help_text="youtu.be/XXXXX の XXXXX 部分")
    label      = models.CharField("ラベル（管理用メモ）", max_length=100, blank=True)
    is_active  = models.BooleanField("表示する", default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "YouTube ライブ"
        verbose_name_plural = "YouTube ライブ一覧"

    def __str__(self):
        return f"{self.label or self.video_id} ({'表示中' if self.is_active else '非表示'})"


class Blog(models.Model):
     # 画像フィールド：upload_toで保存先フォルダを指定
    image = models.ImageField(upload_to='blog_photos/', verbose_name="投稿画像")
    
    # 日付フィールド：デフォルトで現在の投稿時刻が入る
    post_date = models.DateField(default=timezone.now, verbose_name="投稿日")
    
    # 説明文フィールド
    description = models.TextField(max_length=500, verbose_name="説明文")
    
    # 管理画面で見やすくするための設定
    def __str__(self):
        return f"{self.post_date} の投稿"

    class Meta:
        verbose_name = "ブログ投稿"
        verbose_name_plural = "ブログ投稿一覧"
        ordering = ['-id']  # 新しい投稿が上にくるように設定