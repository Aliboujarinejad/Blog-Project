from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="نویسنده")
    content = models.TextField(verbose_name="محتوا")
    image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True, null=True, verbose_name='تصویر')

    STATUS_CHOICES = (
        ('draft','پیش نویس'),
        ('published','منتشر شده'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='وضعیت')

    published_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    slug = models.SlugField(max_length=200, unique=True, verbose_name="اسلاگ")

    class Meta:
        ordering = ['-published_date']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", args=[self.slug])
    

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='connents', 
        verbose_name="مقاله")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True, 
        related_name='connents', 
        verbose_name="کاربر")
    
    body = models.TextField(verbose_name="متن نظر")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    active = models.BooleanField(default=True, verbose_name="فعال")


    class Meta:
        ordering = ['created_date']
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
    
    def __str__(self):
        return f'نظر {self.name} روی {self.post.title}'