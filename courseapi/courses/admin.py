from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from .models import Category,Course, Lesson
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'


class MyLessonAdmin(ModelAdmin):
    form = LessonForm


class MyCourseAdmin(ModelAdmin):
    readonly_fields = ['image_view']
    def image_view(self,courses):
        if courses:
            return mark_safe(f'<img src="/static/{courses.image.name}" width="120" />')



class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [path('course-stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()

        stats = Course.objects \
            .annotate(lesson_count=Count('lessons')) \
            .values('id', 'subject', 'lesson_count')
        return TemplateResponse(request,
                                'admin/course-stats.html',
                                {'course_count': count,'course_stats': stats})

admin_site = CourseAppAdminSite(name='myadmin')
admin_site.register(Category)
# admin.site.register(Category)
# admin_site.register(Course, MyCourseAdmin)
# admin.site.register(Lesson,MyLessonAdmin)
