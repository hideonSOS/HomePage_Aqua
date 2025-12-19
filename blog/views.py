from django.shortcuts import render
from input_page.models import Blog

def blog_timeline(request):
    # データベースからすべての投稿を日付順（新しい順）に取得
    posts = Blog.objects.all().order_by('-id')
    
    # テンプレート（HTML）に'posts'という名前でデータを渡す
    return render(request, 'blog/blogpage.html', {'posts': posts})