from django.db import models

# Create your models here.
from accounts.models import AuthUser


class BoardSe005930(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    contents = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True, null=False)
    hits = models.IntegerField(null=False, default=0)
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'board_se005930'

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()