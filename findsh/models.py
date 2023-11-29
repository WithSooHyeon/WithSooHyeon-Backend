from django.db import models

class FindSH(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    promise_date = models.DateTimeField(auto_now_add=False, null=True)
    place = models.CharField(max_length=20)
    age_group= models.IntegerField(default=20)
    gender = models.IntegerField(default=20)
    num = models.IntegerField(default=1)
    fee = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    interest_count = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    free_condition = models.TextField(max_length=100)