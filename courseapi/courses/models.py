from importlib.metadata import requires

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# việc đâu tiên
class User(AbstractUser):
    avatar = CloudinaryField()

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Course(BaseModel):
    subject = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = CloudinaryField()
    category = models.ForeignKey('Category',on_delete=models.PROTECT)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-id']

class Lesson(BaseModel):
    subjects = models.CharField(max_length=255)
    content = RichTextField()
    image = CloudinaryField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='lessons')
    tags = models.ManyToManyField('Tag',related_name='lessons')

    def __str__(self):
        return self.subjects

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Interaction(BaseModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='comments')
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE, related_name='comments')

class Comment(Interaction):
    content = models.TextField()

class Like(Interaction):
    class Meta:
        unique_together = ('lesson', 'user')



