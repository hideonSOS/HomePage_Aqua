from django.forms import ModelForm
from .models import Schedule
import django.forms as forms
from .models import Blog


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
                'placeholder': '前半スタジオ解説者を入力',
            }
        ),
        'artist2': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': '後半スタジオ解説者を入力',
            }
        ),
        'artist3': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': 'MCを入力',
            }
        ),'artist4': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': 'ゲスト出演者を入力',
            }
        ),
    }
        

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['image', 'post_date', 'description']
        widgets = {
            'post_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': '説明文を入力してください'}),
        }