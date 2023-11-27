from django.shortcuts import render
from .models import Counsel, Comment, Reply
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .serializers import CounselModelSerializer, CommentModelSefializer, CommentListModelSerializer, ReplyModelSefializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

class CounselViewSet(ModelViewSet):
    queryset = Counsel.objects.all().order_by('-created_at')
    serializer_class = CounselModelSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content'] # ?search= -> QuerySet 조건 절에 추가할 필드 지정. 모델 필드 중에 문자열 필드만을 지정.
    ordering_fields = ['view','comments'] # ?ordering= -> 정렬을 허용할 필드의 화이트 리스트. 미지정 시에 serializer_class에 지정된 필드들.

    def perform_create(self, serializer):
        serializer.save(
            writer=self.request.user,
        )

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        # 당일날 밤 12시에 쿠키 초기화
        tomorrow = datetime.datetime.replace(timezone.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        
        # response를 미리 받고 쿠키를 만들어야 한다
        serializer = CounselModelSerializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        # 쿠키 읽기 & 생성
        if request.COOKIES.get('view') is not None: # 쿠키에 hit 값이 이미 있을 경우
            cookies = request.COOKIES.get('view')
            cookies_list = cookies.split('|') # '|'는 다르게 설정 가능 ex) '.'
            if str(pk) not in cookies_list:
                response.set_cookie('view', cookies+f'|{pk}', expires=expires) # 쿠키 생성
                instance.view += 1
                instance.save()
                    
        else: # 쿠키에 view 값이 없을 경우(즉 현재 보는 게시글이 첫 게시글임)
            response.set_cookie('view', pk, expires=expires)
            instance.view += 1
            instance.save()

        # view가 추가되면 해당 instance를 serializer에 표시
        serializer = self.get_serializer(instance)

        return response
    
    @action(detail=True, methods=['get'])
    def get_comment_all(self, reqeust, pk=None):
        counsel = self.get_object()
        comment_all = counsel.comment_set.all()
        serializer = CommentListModelSerializer(comment_all, many = True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        counsel = self.get_object()
        liked_users = counsel.liked_users
        if liked_users.filter(id=request.user.id).exists():
            liked_users.remove(request.user)
            message = 'counsel cancel'
        else:
            liked_users.add(request.user)
            message='counsel like'
        like_count =liked_users.count()
        return Response({'message' : message, 'like_count': like_count})
            

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentModelSefializer

    def perform_create(self, serializer):
        serializer.save(
            writer=self.request.user,
        )
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Counsel.objects.get(pk = request.data['counsel'])
        instance.comments += 1
        instance.save()
        CounselModelSerializer(instance)
        serializer.save(counsel = instance, writer=self.request.user,)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        counsel = self.get_object()
        liked_users = counsel.liked_users
        if liked_users.filter(id=request.user.id).exists():
            liked_users.remove(request.user)
            message = 'comment cancel'
        else:
            liked_users.add(request.user)
            message='comment like'
        like_count =liked_users.count()
        return Response({'message' : message, 'like_count': like_count})
    
class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all().order_by('-created_at')
    serializer_class = ReplyModelSefializer

    def perform_create(self, serializer):
        serializer.save(
            writer=self.request.user,
        )
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Comment.objects.get(pk = request.data['comment'])
        counsel = Counsel.objects.get(pk = request.data['counsel'])
        instance.save()
        CommentModelSefializer(instance)
        serializer.save(counsel = counsel, comment = instance, writer=self.request.user,)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):
        counsel = self.get_object()
        liked_users = counsel.liked_users
        if liked_users.filter(id=request.user.id).exists():
            liked_users.remove(request.user)
            message = 'reply cancel'
        else:
            liked_users.add(request.user)
            message='reply like'
        like_count =liked_users.count()
        return Response({'message' : message, 'like_count': like_count})
        