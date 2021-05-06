from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Friendship(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        # 此处related_name是一定要加的，原因是在Friendship中有两个fields都用到了User
        # 那么在用user.friendship_set引用时 会不明确此处的user是来自from_user还是to_user
        # 在添加了related_name之后，使用的时候就不是user_friendship_set，而是user.following_friendship_set
        related_name='following_friendship_set',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        # 同上
        related_name="follower_friendship_set",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            # 获得用户关注的所有人，按照关注时间排序
            ('from_user', 'created_at'),
            # 获得关注用户的所有人， 按照关注时间排序
            ('to_user', 'created_at'),
        )
        # 唯一索引是为了防止重复关注同一个人
        unique_together = (('from_user', 'to_user'),)

    def __str__(self):
        return f'{self.from_user_id} followed {self.to_user_id}'
