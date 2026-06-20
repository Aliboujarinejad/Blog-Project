# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import CommentForm  # بعداً می‌سازیمش


def post_list(request):
    """نمایش لیست تمام مقالات منتشر شده"""
    posts = Post.objects.filter(status='published')
    
    # صفحه‌بندی (هر صفحه ۵ مقاله)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'لیست مقالات',
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """نمایش جزئیات یک مقاله به همراه نظرات"""
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.connents.filter(active=True)  # توجه: در مدل شما 'connents' نوشته شده
    
    # فرم نظر
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'title': post.title,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def post_create(request):
    """ایجاد مقاله جدید (فقط کاربران لاگین شده)"""
    if request.method == 'POST':
        # اینجا باید فرم ایجاد مقاله رو پردازش کنید
        # برای سادگی، یک نمونه ساده می‌نویسم
        title = request.POST.get('title')
        content = request.POST.get('content')
        slug = request.POST.get('slug')
        status = request.POST.get('status', 'draft')
        image = request.FILES.get('image')
        
        post = Post.objects.create(
            title=title,
            content=content,
            slug=slug,
            status=status,
            image=image,
            author=request.user
        )
        messages.success(request, 'مقاله با موفقیت ایجاد شد.')
        return redirect('post_detail', slug=post.slug)
    
    return render(request, 'blog/post_create.html', {'title': 'ایجاد مقاله جدید'})


@login_required
def post_edit(request, slug):
    """ویرایش مقاله (فقط نویسنده)"""
    post = get_object_or_404(Post, slug=slug)
    
    # بررسی اینکه کاربر نویسنده مقاله باشد
    if post.author != request.user:
        messages.error(request, 'شما اجازه ویرایش این مقاله را ندارید.')
        return redirect('post_detail', slug=post.slug)
    
    if request.method == 'POST':
        # پردازش ویرایش
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.status = request.POST.get('status', post.status)
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        messages.success(request, 'مقاله با موفقیت ویرایش شد.')
        return redirect('post_detail', slug=post.slug)
    
    context = {
        'post': post,
        'title': f'ویرایش: {post.title}',
    }
    return render(request, 'blog/post_edit.html', context)


def search_posts(request):
    """جستجوی مقالات"""
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            status='published',
            title__icontains=query
        ) | Post.objects.filter(
            status='published',
            content__icontains=query
        )
    else:
        posts = Post.objects.none()
    
    context = {
        'posts': posts,
        'query': query,
        'title': f'نتایج جستجو برای: {query}',
    }
    return render(request, 'blog/search_results.html', context)