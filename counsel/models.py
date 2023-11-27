from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Counsel(models.Model):
    title = models.TextField("제목", default="")
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성날짜", auto_now_add=True)
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    scraps = models.IntegerField(default = 0)
    comments = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(User, through='Counsel_like', related_name='liked_counsel')

class Counsel_scrap(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    counsel = models.ForeignKey(to=Counsel, on_delete=models.CASCADE, default="")

class Counsel_like(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    counsel = models.ForeignKey(to=Counsel, on_delete=models.CASCADE, default="")


class Comment(models.Model):
    counsel = models.ForeignKey(to=Counsel, on_delete=models.CASCADE)
    content = models.TextField("댓글내용")
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True )
    created_at = models.DateTimeField("생성날짜", auto_now_add=True)
    replies = models.IntegerField(default=0) 
    liked_users = models.ManyToManyField(User, through='Comment_like', related_name='liked_comment')

class Comment_like(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, default="")

class Reply(models.Model):
    counsel = models.ForeignKey(to=Counsel, on_delete=models.CASCADE, default="")
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    content = models.TextField("댓글내용")
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True )
    created_at = models.DateTimeField("생성날짜", auto_now_add=True)
    liked_users = models.ManyToManyField(User, through='Reply_like', related_name='liked_reply')

class Reply_like(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(to=Reply, on_delete=models.CASCADE, default="")