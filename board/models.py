from django.db import models

# Create your models here.
from MyStock import settings
from accounts.models import AuthUser
from pytz import timezone

class BoardSe005930(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    contents = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True, null=False)
    hits = models.IntegerField(null=False, default=0)
    username = models.CharField(max_length=150)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.registered_date.astimezone(korean_timezone)

    class Meta:
        managed = False
        db_table = 'board_se005930'

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()

class CommentSe005930(models.Model):
    pid = models.OneToOneField(BoardSe005930, models.DO_NOTHING, db_column='pid', primary_key=True)
    uid = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    comments = models.TextField()
    username = models.CharField(max_length=150)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.created_date.astimezone(korean_timezone)

    class Meta:
        managed = False
        db_table = 'comment_se005930'
        unique_together = (('pid', 'uid', 'created_date'),)