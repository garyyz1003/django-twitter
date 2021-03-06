from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now
from likes.models import Like
from django.contrib.contenttypes.models import ContentType
# from comments.models import Comment

# django 内部支持的一种方法：
# user.tweet_set 等价于
# Tweet.objects.filter(user=user)


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
    # 上述创建user的时候没有创建related_name是因为该model中只有一个 field用到了User
    # 在有多个fields用到User的时候需要添加related_name
    # 参考 friendships 中的model
    content = models.CharField(max_length=255)
    # auto_now 创建的时候自动把当前时间填入
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 建立联合索引
        # 如果要建立单独索引， 可以在对应的field里添加属性 db_index=True
        index_together = (('user', 'created_at'),)
        # 指定默认的排序规则 对数据库没有影响
        # 建立完索引后需要做 makemigrations 和 migrate
        ordering = ('user', '-created_at')

    @property
    def hours_to_now(self):
        # datetime.now() 不带时区信息。 需要增加上utc的时区信息
        return (utc_now() - self.created_at).seconds // 3600

    # 也可以用如下的方法得到tweet的comment
    # @property
    # def comments(self):
    #     return self.comment_set.all()
    # return Comment.objects.filter(tweet=self)

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Tweet),
            object_id=self.id,
        ).order_by('-created_at')

    def __str__(self):
        # 这里是执行print(Tweet instance)的时候显示的内容
        # python3.0 format的写法 f'{variable}'
        return f'{self.created_at} {self.user} {self.content}'
