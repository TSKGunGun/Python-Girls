import re
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib import messages

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    return render(request, 'blog/post_list.html', {'posts' : posts } )

def post_detail(request, post_id):
    post = get_object_or_404(Post,pk=post_id)
    
    return render(request, "blog/post_detail.html", {'post' : post})

def post_new(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid() :
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            
            messages.success(request, "新規投稿が完了しました。")
            return redirect('post_detail', post_id=post.pk)
        else:
            messages.error(request,"新規投稿に失敗しました。")
    else:
        form = PostForm()
        return render(request, "blog/post_edit.html", {'form': form})
    
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method=="POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid() :
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            
            messages.success(request, "投稿の更新が完了しました。")
            return redirect('post_detail', post_id=post.pk)
        else:
            messages.error(request,"投稿の更新に失敗しました。")
    else:
        form = PostForm(instance=post)
        return render(request, "blog/post_edit.html", {'form': form})