from django.forms import ModelForm
from .models import Schedule
import django.forms as forms


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['day','title','time','artist1','artist2','artist3','artist4']
        
        widgets = {
        'day': forms.DateInput(
            attrs={
                'type': 'date',
                'id': 'input-day',              # ← ここでidを指定
                'class': 'form-control date',   # ← classもOK
                'placeholder': '日付を選択',
            }
        ),
        'title': forms.TextInput(
            attrs={
                'id': 'input-title',
                'class': 'form-control',
                'placeholder': '開催タイトルを入力',
            }
        ),
        'time': forms.TextInput(
            attrs={
                'id': 'input-time',
                'class': 'form-control',
                'placeholder': '配信開始時刻～終了時刻を入力',
            }
        ),
        'artist1': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': '出演者を入力',
            }
        ),
        'artist2': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': '出演者を入力',
            }
        ),
        'artist3': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': '出演者を入力',
            }
        ),'artist4': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': '出演者を入力',
            }
        ),
    }
        