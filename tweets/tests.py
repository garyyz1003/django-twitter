from django.test import TestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now


class TweetTests(TestCase):

    def test_hours_to_now(self):
        garyyz = User.objects.create_user(username='garyyz')
        tweet = Tweet.objects.create(user=garyyz, content='LALALA')
        tweet.created_at = utc_now() - timedelta(hours=5)
        tweet.save()
        self.assertEqual(tweet.hours_to_now, 5)

