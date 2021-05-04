from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now


class Tweet(models.Model):
    # who posts this tweet
    # help_text 会在django中也显示注释
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text='who posts this tweet',
        verbose_name='Tweet Poster'
    )
    content = models.CharField(max_length=255)
    # auto_now 创建的时候自动把当前时间填入
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def hours_to_now(self):
        # datetime.now() 不带时区信息。 需要增加上utc的时区信息
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        # 这里是执行print(Tweet instance)的时候显示的内容
        # python3.0 format的写法 f'{variable}'
        return f'{self.created_at} {self.user} {self.content}'