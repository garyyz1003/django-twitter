from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Like(models.Model):
    # 点赞的用户和时间必不可少
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # 由于点赞是可以既给tweet也可以给comment 点赞的 我们希望只建立一个field来同时满足这两种需求
    # 考虑是否可以用一个通用的foreignkey
    # 这里引入django自带的content type -- 本质上是一个表单，里面记录了所有的model
    # https://docs.djangoproject.com/en/3.1/ref/contrib/contenttypes/#generic-relations
    object_id = models.PositiveIntegerField() # tweet_id or comment_id
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
    )
    # content_object只是提供一个快捷的访问方法 可以允许用户用like 的instance查询对应的内容类别
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        # 限制每个用户在一个tweet或comment下只能点击一个赞
        unique_together = (('user', 'content_type', 'object_id'),)
        # 这个 index 的作用是可以按时间排序某个被like的content_object 的所有likes
        # 并且可以查询某个用户在哪些tweet/comment 下点了赞
        index_together = (
            ('content_type', 'object_id', 'created_at'),
            ('user', 'content_type', "created_at"),
        )

    def __str__(self):
        return '{} - {} liked {} {}'.format(
            self.created_at,
            self.user,
            self.content_type,
            self.content_type_id,
        )