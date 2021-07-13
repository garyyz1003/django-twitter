from testing.testcases import TestCase

# Create your tests here.
class CommentModelTests(TestCase):

    def setUp(self):
        self.user = self.create_user('gary')
        self.tweet = self.create_tweet(self.user)
        self.comment = self.create_comment(self.user, self.tweet)

    def test_comment(self):
        self.assertNotEqual(self.comment.__str__(), None)

    def test_like_set(self):
        self.create_like(self.user, self.comment)
        self.assertEqual(self.comment.like_set.count(), 1)

        self.create_like(self.user, self.comment)
        self.assertEqual(self.comment.like_set.count(), 1)

        chenmo = self.create_user('chenmo')
        self.create_like(chenmo, self.comment)
        self.assertEqual(self.comment.like_set.count(), 2)
