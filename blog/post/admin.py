from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست مقالات نمایش داده میشن
    list_display = ('title', 'author', 'status', 'published_date', 'created_date')
    
    # فیلترهای سمت راست صفحه
    list_filter = ('status', 'author', 'published_date', 'created_date')
    
    # فیلدهای جستجو
    search_fields = ('title', 'content', 'author__username')
    
    # اسلاگ به صورت خودکار از عنوان پر میشه
    prepopulated_fields = {'slug': ('title',)}
    
    # تاریخ‌ها به صورت سلسله‌مراتبی نمایش داده میشن
    date_hierarchy = 'published_date'
    
    # ترتیب پیش‌فرض (جدیدترین اول)
    ordering = ('-published_date',)
    
    # گروه‌بندی فیلدها در صفحه ویرایش
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'author', 'content', 'image')
        }),
        ('وضعیت انتشار', {
            'fields': ('status', 'published_date')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)  # این بخش قابل جمع شدن هست
        }),
    )
    
    # فیلدهایی که فقط خواندنی هستن
    readonly_fields = ('created_date', 'updated_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # ستون‌های نمایش داده شده
    list_display = ('name', 'post', 'user', 'created_date', 'active')
    
    # فیلترها
    list_filter = ('active', 'created_date', 'post')
    
    # جستجو
    search_fields = ('name', 'email', 'body', 'post__title')
    
    # قابلیت ویرایش سریع در صفحه لیست
    list_editable = ('active',)
    
    # ترتیب
    ordering = ('-created_date',)
    
    # اکشن‌های سفارشی (اختیاری)
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, "نظرات انتخاب شده فعال شدن.")
    make_active.short_description = "فعال کردن نظرات انتخاب شده"
    
    def make_inactive(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, "نظرات انتخاب شده غیرفعال شدن.")
    make_inactive.short_description = "غیرفعال کردن نظرات انتخاب شده"
    
    # نمایش نام کاربر به جای شیء
    def name(self, obj):
        if obj.user:
            return obj.user.username
        return "کاربر مهمان"
    name.short_description = "نام کاربر"