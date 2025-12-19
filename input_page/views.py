from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
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


class ScheduleUpdateView(TemplateView):
    template_name = "input_page/update.html"


from .models import Blog
from .forms import BlogForm # 後ほどforms.pyで定義します

# --- ブログ投稿 (Create) ---
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
def blog_list(request):
    posts = Blog.objects.all().order_by('-id')
    return render(request, 'input_page/blog_list.html', {'posts': posts})

# --- ブログ編集 (Update) ---
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
def blog_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('input_page:blog_list')
    return render(request, 'input_page/blog_delete.html', {'post': post})