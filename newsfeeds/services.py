from friendships.services import FriendshipService
from newsfeeds.models import NewsFeed


class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
        # 错误的方法
        # 在production 是不允许for + query的 效率很低
        # 原因是 web server和 db通常不在一台机器上 多次查询会产生大量延迟 (round trip多 -- 用户信息的验证)

        # for follower in FriendshipService.get_followers(tweet.user):
        #     NewsFeed.objects.create(
        #         user=follower,
        #         tweet=tweet,
        #     )

        # 正确的方法： 使用bulk_create, 会把insert语句合成一条
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)  # 由于此处没有.save 所以不会产生数据库存储请求操作
            for follower in FriendshipService.get_followers(tweet.user)
        ]
        # 由于用户自己不是自己的follower
        # 此处是把用户本身也加入到follower中使得自己也可以看到自己的newsfeed
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        NewsFeed.objects.bulk_create(newsfeeds)