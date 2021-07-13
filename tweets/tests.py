from django.test import TestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now
from testing.testcases import TestCase


class TweetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='garyyz')
        self.tweet = Tweet.objects.create(user=self.user, content='LALALA')

    def test_hours_to_now(self):
        self.tweet.created_at = utc_now() - timedelta(hours=5)
        self.tweet.save()
        self.assertEqual(self.tweet.hours_to_now, 5)

    def test_like_set(self):
        self.create_like(self.user, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        self.create_like(self.user, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        chenmo = self.create_user('chenmo')
        self.create_like(chenmo, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)

