from django.test import TestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now


class TweetTests(TestCase):

    def test_hours_to_now(self):
        garyyz = User.objects.create_user(username='garyyz')
        tweet = Tweet.objects.create(user=garyyz, content='LALALA')
        print(f'utc_time: {utc_now()}')
        tweet.created_at = utc_now() - timedelta(hours=5)
        print(f'tweet_time: {tweet.created_at}')
        tweet.save()
        print(f'tweet_time: {tweet.created_at}')
        print((utc_now() - tweet.created_at).seconds)
        self.assertEqual(tweet.hours_to_now, 5)

