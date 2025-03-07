# from django.contrib import admin
from django.urls import path, include
from . import views
# from courses.admin import admin_site
from rest_framework.routers import DefaultRouter

routes = DefaultRouter()
routes.register('categories', views.CategoryViewset, basename='category')
routes.register('courses', views.CourseViewset, basename='course')
routes.register('lessons', views.LessonViewset, basename='lesson')

urlpatterns = [
    path('', include(routes.urls)),

]

