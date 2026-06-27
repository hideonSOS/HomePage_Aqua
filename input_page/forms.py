from django.forms import ModelForm
from .models import Schedule
import django.forms as forms
from .models import Blog, SlideImage
import json
import os
import re


def _time_choices():
    choices = [('', '--- 時刻を選択 ---')]
    for h in range(6, 24):
        for m in range(0, 60, 10):
            t = f"{h:02d}:{m:02d}"
            choices.append((t, t))
    return choices

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
    time_start = forms.ChoiceField(
        choices=_time_choices(),
        label='開始時刻',
        required=False,
        widget=forms.Select(attrs={'id': 'input-time-start', 'class': 'form-control time-select'}),
    )
    time_end = forms.ChoiceField(
        choices=_time_choices(),
        label='終了時刻',
        required=False,
        widget=forms.Select(attrs={'id': 'input-time-end', 'class': 'form-control time-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        # 編集時: 既存の time 文字列を start/end に分解してセット
        if self.instance and self.instance.pk and self.instance.time:
            parts = self.instance.time.split('〜')
            if len(parts) == 2:
                self.fields['time_start'].initial = parts[0].strip()
                self.fields['time_end'].initial = parts[1].strip()

    def clean(self):
        cleaned = super().clean()
        title = cleaned.get('title', '')
        time_start = cleaned.get('time_start', '')
        time_end = cleaned.get('time_end', '')
        seminar = cleaned.get('seminar', False)

        # タイトルなし（ゼミナールのみの日）の場合のルール
        if not title:
            if not time_start or not time_end:
                raise forms.ValidationError(
                    '住之江ゼミナールのみの日は「配信時刻」を入力してください。'
                )
            if not seminar:
                raise forms.ValidationError(
                    '住之江ゼミナールのみの日は「住之江ゼミナール」のチェックを入れてください。'
                )
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        start = self.cleaned_data.get('time_start', '')
        end = self.cleaned_data.get('time_end', '')
        instance.time = f"{start}〜{end}"
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Schedule
        fields = ['day', 'title', 'seminar', 'artist1', 'artist2', 'artist3', 'artist4']
        labels = {
            'seminar': '住之江ゼミナール（12R終了後～１時間程度）',
            'artist1': '前半スタジオ解説（1〜6R）',
            'artist2': '後半スタジオ解説（7〜12R）',
            'artist3': 'MC',
        }
        widgets = {
        'day': forms.DateInput(
            attrs={
                'type': 'date',
                'id': 'input-day',
                'class': 'form-control date',
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
        'seminar': forms.CheckboxInput(
            attrs={
                'id': 'input-seminar',
                'class': 'seminar-check',
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