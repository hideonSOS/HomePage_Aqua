from django.forms import ModelForm
from .models import Schedule
import django.forms as forms
from .models import Blog, SlideImage
import json
import os
import re

def _load_title_choices():
    json_path = os.path.join(os.path.dirname(__file__), 'static', 'input_page', 'js', 'title_check.json')
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    choices = [('', '--- タイトルを選択 ---')]
    for item in data:
        title = item[4]
        choices.append((title, title))
    return choices

def _load_mc_choices():
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'input_page', 'js', 'persons.js')
    with open(js_path, encoding='utf-8') as f:
        content = f.read()
    block = re.search(r'const MC\s*=\s*\[(.*?)\];', content, re.DOTALL)
    names = re.findall(r'name:\s*"([^"]+)"', block.group(1)) if block else []
    seen = set()
    unique_names = [n for n in names if not (n in seen or seen.add(n))]
    choices = [('', '--- MCを選択 ---')]
    for name in unique_names:
        choices.append((name, name))
    return choices

def _load_kaisetsu_choices():
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'input_page', 'js', 'persons.js')
    with open(js_path, encoding='utf-8') as f:
        content = f.read()
    # const kaisetsu = [ ... ]; ブロックを抽出
    block = re.search(r'const kaisetsu\s*=\s*\[(.*?)\];', content, re.DOTALL)
    names = re.findall(r'name:\s*"([^"]+)"', block.group(1)) if block else []
    # 重複除去（順序維持）
    seen = set()
    unique_names = [n for n in names if not (n in seen or seen.add(n))]
    choices = [('', '--- 解説者を選択 ---')]
    for name in unique_names:
        choices.append((name, name))
    return choices


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
        'title': forms.Select(
            choices=_load_title_choices(),
            attrs={
                'id': 'input-title',
                'class': 'form-control',
            }
        ),
        'time': forms.TextInput(
            attrs={
                'id': 'input-time',
                'class': 'form-control',
                'placeholder': '配信開始時刻～終了時刻を入力',
            }
        ),
        'artist1': forms.Select(
            choices=_load_kaisetsu_choices(),
            attrs={
                'id': 'input-artist1',
                'class': 'form-control',
            }
        ),
        'artist2': forms.Select(
            choices=_load_kaisetsu_choices(),
            attrs={
                'id': 'input-artist2',
                'class': 'form-control',
            }
        ),
        'artist3': forms.Select(
            choices=_load_mc_choices(),
            attrs={
                'id': 'input-artist3',
                'class': 'form-control',
            }
        ),
        'artist4': forms.Textarea(
            attrs={
                'id': 'input-artist',
                'class': 'form-control',
                'placeholder': 'ゲスト出演者を入力',
                'rows': 1,
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


class SlideImageForm(forms.ModelForm):
    class Meta:
        model = SlideImage
        fields = ['image', 'order']
        widgets = {
            'order': forms.NumberInput(attrs={'placeholder': '表示順（小さい数字が先）', 'min': 0}),
        }