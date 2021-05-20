from friendships.models import Friendship
from django.contrib.auth.models import User

class FriendshipService(object):

    @classmethod
    def get_followers(self, user):
        # 错误的写法一
        # 这种写法会导致 N + 1 Queries 的问题
        # 即， filter 出所有friendships 耗费了一次 Query
        # 而 for 循环每个 friendship 取 from_user 又耗费了N次 Queries
        # friendships = Friendship.objects.filter(to_user=user)
        # return [friendship.from_user for friendship in friendships]

        # 错误的写法二
        # 这种写法是使用了join操作 让 friendship table 和 user table 在from_user
        # 这个属性上 join 了起来， join 操作在大规模用户的 web 场景下是禁用的， 因为非常慢
        # friendships = Friendship.objects.filter(
        #     to_user=user
        # ).select_related('from_user')
        # return [friendship.from_user for friendship in friendships]

        # 正确的写法一， 自己手动filter id， 使用 IN query 查询
        # friendships = Friendship.objects.filter(to_user=user)
        # follower_ids = [friendships.from_user_id for friendship in friendships]
        # followers = User.objects.filter(id__in=follower_ids)

        # 正确的写法二， 使用prefetch_related, 会自动执行成两条语句， 用in query 查询
        # 实际执行的SQL 查询和上面是一样， 一共两条SQL Queries
        friendships = Friendship.objects.filter(
            to_user=user,
        ).prefetch_related('from_user')
        return [friendships.from_user for friendship in friendships]
