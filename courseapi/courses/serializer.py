from rest_framework import serializers
from courses.models import Category,Course, Lesson, Tag,Comment,User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class UserSelializer(serializers.ModelSerializer):
    class Meta:
        model = User

class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        cloud_name = "dnzjjdg0v"
        # data['image'] = f"https://res.cloudinary.com/{cloud_name}/{data['image']}"
        data['image'] = instance.image.url
        return data

class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject','image','created_date','category_id']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']

class LessonSerializer(BaseSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ['id','subjects','image', 'course_id','created_date','update_date']

class LessonDetailSerializer(LessonSerializer):
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content','tags']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content','created_date','update_date','user']


