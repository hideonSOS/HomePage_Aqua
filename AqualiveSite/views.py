from django.views.generic import View, TemplateView
from django.shortcuts import render
from input_page.models import Schedule
import pandas as pd
from input_page.models import SlideImage # ★追加：スライド画像のモデル

def indexView(request):
    # ==========================================
    # 1. 既存の処理（カレンダー情報の取得）
    # ==========================================
    schedules = Schedule.objects.values('day', 'title', 'time', 'artist')
    
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
    ctx = {
        'data': list(schedules),        # 既存：カレンダー用データ
        'hero_images_data': slide_list, # ★追加：スライド用データ
    }
    
    return render(request, 'index.html', ctx)