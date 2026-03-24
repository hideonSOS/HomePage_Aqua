from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Schedule
from .forms import ScheduleForm

class ScheduleShow(TemplateView):
    template_name = 'input_page/input_page.html'


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'input_page/input.html'
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('input_page:input')
    login_url='/input_page/login/'


class ScheduleListView(LoginRequiredMixin,ListView):
    template_name = "input_page/list.html"
    model = Schedule
    login_url='/input_page/login/'
    context_object_name = 'schedule_list'
    

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "input_page/delete.html"
    model = Schedule
    success_url = reverse_lazy('input_page:list')
    login_url='/input_page/login/'


class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "input_page/update.html"
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('input_page:list')
    login_url = '/input_page/login/'


from django.db.models import Count
from .models import Blog, AccessLog


@login_required(login_url='/input_page/login/')
def access_counter(request):
    total = AccessLog.objects.count()
    by_page = (
        AccessLog.objects
        .values('page')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    return render(request, 'input_page/access_counter.html', {
        'total': total,
        'by_page': by_page,
    })


from .models import Blog, SlideImage, YouTubeLive
from .forms import BlogForm, SlideImageForm

# --- ブログ投稿 (Create) ---
@login_required(login_url='/input_page/login/')
def blog_input(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('input_page:blog_input') # 再び入力画面に戻る
    else:
        form = BlogForm()
    
    # 閲覧ページと同じように、過去の投稿を取得して渡す
    posts = Blog.objects.all().order_by('-id')
    
    return render(request, 'input_page/blog_input.html', {
        'form': form,
        'posts': posts, # これで閲覧ページと同じループが使えるようになります
    })

# --- ブログ一覧（管理者用・編集削除ボタンあり） (Read) ---
@login_required(login_url='/input_page/login/')
def blog_list(request):
    posts = Blog.objects.all().order_by('-id')
    return render(request, 'input_page/blog_list.html', {'posts': posts})

# --- ブログ編集 (Update) ---
@login_required(login_url='/input_page/login/')
def blog_update(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('input_page:blog_list')
    else:
        form = BlogForm(instance=post)
    return render(request, 'input_page/blog_update.html', {'form': form, 'post': post})

# --- ブログ削除 (Delete) ---
@login_required(login_url='/input_page/login/')
def blog_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        post.delete()
        next_url = request.POST.get('next', 'input_page:blog_list')
        return redirect(next_url)
    return render(request, 'input_page/blog_delete.html', {'post': post})


# --- スライド管理 ---
@login_required(login_url='/input_page/login/')
def slide_manage(request):
    if request.method == 'POST':
        form = SlideImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('input_page:slide_manage')
    else:
        form = SlideImageForm()
    slides = SlideImage.objects.all().order_by('order')
    return render(request, 'input_page/slide_manage.html', {'form': form, 'slides': slides})


@login_required(login_url='/input_page/login/')
def slide_delete(request, pk):
    slide = get_object_or_404(SlideImage, pk=pk)
    if request.method == 'POST':
        slide.image.delete(save=False)
        slide.delete()
    return redirect('input_page:slide_manage')


# --- YouTube ライブ管理 ---
@login_required(login_url='/input_page/login/')
def youtube_live_manage(request):
    current = YouTubeLive.objects.order_by('-updated_at').first()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save':
            video_id = request.POST.get('video_id', '').strip()
            label    = request.POST.get('label', '').strip()
            if video_id:
                if current:
                    current.video_id  = video_id
                    current.label     = label
                    current.is_active = True
                    current.save()
                else:
                    YouTubeLive.objects.create(video_id=video_id, label=label, is_active=True)

        elif action == 'deactivate':
            YouTubeLive.objects.update(is_active=False)

        elif action == 'activate':
            if current:
                current.is_active = True
                current.save()

        elif action == 'delete':
            if current:
                current.delete()

        return redirect('input_page:youtube_live_manage')

    return render(request, 'input_page/youtube_live.html', {'current': current})