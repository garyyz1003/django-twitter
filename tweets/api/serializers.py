from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserSerializer
from accounts.api.serializers import UserSerializerForTweet
from comments.api.serializers import CommentSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')


class TweetSerializerWithComments(serializers.ModelSerializer):
    user = UserSerializer()
    # <HOMEWORK> 使用 serializer.SerializerMethodField 的方式实现comments
    comments = CommentSerializer(source='comment_set', many=True)

    # <HOMEWORK实现>
    # comments = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'comments', 'created_at', 'content')

    # <HOMEWORK实现>
    # def get_comments(self, obj):
    #     return CommentSerializer(obj.comments_set.all(), many=True).data


class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet
