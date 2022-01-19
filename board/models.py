# Create your models here.
#from django.contrib.auth import models
from django.contrib.auth import models
from django.db import models
from MyStock import settings
from accounts.models import AuthUser
from pytz import timezone

class Board(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=120)
    contents = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True, null=False)
    hits = models.IntegerField(null=False, default=0)
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'board'
    @property
    def increase_hits(self):
        self.hits += 1
        self.save()

class Comment(models.Model):
    pid = models.ForeignKey(Board, models.DO_NOTHING, db_column='pid')
    uid = models.IntegerField()
    comment_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    comments = models.TextField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'comment'