from django.views.generic import View, TemplateView
from django.shortcuts import render
from input_page.models import Schedule
import pandas as pd
from input_page.models import SlideImage, YouTubeLive
from input_page.ticker_store import get_ticker

def indexView(request):
    # ==========================================
    # 1. 既存の処理（カレンダー情報の取得）
    # ==========================================
    schedules = Schedule.objects.values('day', 'title', 'time', 'seminar', 'artist1', 'artist2', 'artist3', 'artist4')
    
    # DataFrameの処理（print確認用としてそのまま残します）
    df = pd.DataFrame.from_records(schedules)
    if not df.empty:
        df.drop_duplicates(subset=['day'], keep='last', inplace=True)
    print(df)

    # ==========================================
    # 2. 追加の処理（スライド画像の取得）
    # ==========================================
    slides_query = SlideImage.objects.all().order_by('order')
    
    slide_list = []
    for slide in slides_query:
        if slide.image:
            slide_list.append({
                'url': slide.image.url,
                # titleなどが不要になったのでurlだけでOK
            })

    # ==========================================
    # 3. テンプレートへ渡すデータの作成
    # ==========================================
    yt_live = YouTubeLive.objects.filter(is_active=True).order_by('-updated_at').first()
    youtube_video_id = yt_live.video_id if yt_live else None

    ctx = {
        'data': list(schedules),
        'hero_images_data': slide_list,
        'youtube_video_id': youtube_video_id,
        'ticker_text': get_ticker(),
    }
    
    return render(request, 'index.html', ctx)