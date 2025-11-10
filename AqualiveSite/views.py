from django.views.generic import View, TemplateView
from django.shortcuts import render
from input_page.models import Schedule
import pandas as pd

# class indexView(View):
#     template_name = 'index.html'
    
# class indexView(TemplateView):
#     template_name = 'index.html'

def indexView(request):
    schedules = Schedule.objects.values('day', 'title', 'time', 'artist')  # 必要な項目だけ抽出
    df = pd.DataFrame.from_records(schedules)
    df.drop_duplicates(subset = ['day'], keep='last', inplace=True)
    ctx = {'data': list(schedules)}
    ctxtest = {'day': [i for i in df['day']],
        'title':[i for i in df['title']],
        'time':[i for i in df['time']],
        'artist':[i for i in df['artist']],
        }
    print(df)
    
    return render(request,'index.html', ctx)