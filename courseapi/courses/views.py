from rest_framework import viewsets, generics, status, parsers, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category,Course,Lesson, User
from courses import serializer
from courses import paginators

class CategoryViewset(viewsets.ViewSet,generics.ListAPIView):
    queryset = Category.objects.filter(active = True)
    serializer_class = serializer.CategorySerializer

class CourseViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active = True)
    serializer_class = serializer.CourseSerializer
    pagination_class = paginators.CoursePaginater

    def get_queryset(self):
        queryset = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(subject__icontains = q)
        cate_id = self.request.query_params.get('cate_id')
        if cate_id:
            queryset = queryset.filter(category_id = cate_id)
        return queryset

    @action(detail=True, methods=['get'],url_path="lessons")
    def lessons(self, request, pk=None):
        lessons = self.get_object().lessons.filter(active=True)
        return Response(serializer.LessonSerializer(lessons,many=True).data, status= status.HTTP_200_OK)


#prefetch_related() lấy truocws các tags hệu suất hơn
class LessonViewset(viewsets.ViewSet,generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related().filter(active =True)  # Sửa get() -> all()
    serializer_class = serializer.LessonDetailSerializer

    def get_permissions(self):
        if self.action.__eq__('get_comment') and self.request.method.__eq__('POST'):
            return  [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


    @action(methods=['get', 'post'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            u = serializers.CommentSerializer(data = {
                'content' : request.data.get('content'),
                'user' : request.user.pk,
                'lesson' : pk
            })
            u.is_valid()
            c= u.save()


        else:
            comments = self.get_object().comment_set.select_related('user').filter(active=True)
            return Response(serializer.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializer.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @action(methods=['get', 'patch'], url_path="current-user", detail=False, permission_classes = [permissions.IsAuthenticated])
    def get_current_user(self, request):
        if request.method.__eq__("PATCH"):
            u = request.user

            for key in request.data:
                if key in ['first_name', 'last_name']:
                    setattr(u, key , request.data[key])
                elif key.__eq__('password'):
                    u.set_password(request.data[key])
            u.save()
            return Response(serializers.UserSerializer(u).data)
        else:
            return Response(serializer.UserSerializer(request.user).data)


