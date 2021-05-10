from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet


class NewsFeed(models.Model):
    # 注意此处的user指的不是谁发的贴 而是谁能看到该帖子（tweet）
    # on_delete=models.SET_NULL 否则默认是cascade会产生级联删除
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)  # 此处限定排序是按照用户的newsfeed排列
        unique_together = (('user', 'tweet'),)  # 此处限定同一个用户不能看到两条相同的tweet
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'

