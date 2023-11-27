from rest_framework import serializers
from .models import Counsel, Comment, Reply

# Create your views here.

class CommentListModelSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source = 'liked_users.count', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
    
    def get_reply(self, obj):
        reply = Reply.objects.filter(comment = obj)
        return ReplyModelSefializer(instance=reply, many=True, context=self.context).data
    
class CounselModelSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source = 'liked_users.count', read_only=True)
    class Meta:
        model = Counsel
        fields = '__all__'
        depth=1
    
    def get_comments(self, obj):
        return obj.comment_set.all().count() + obj.reply_set.all().count()

class CommentModelSefializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source = 'liked_users.count', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class ReplyModelSefializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source = 'liked_users.count', read_only=True)
    class Meta:
        model = Reply
        fields = '__all__'
    
