from accounts.api.serializers import UserSerializerForComment
from comments.models import Comment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tweets.models import Tweet


class CommentSerializer(serializers.ModelSerializer):
    # 如果此处不定义user的话，fields中的user会以user_id的形式显示
    # 使用了UserSerializer之后就会用UserSerializer的格式来显示user
    user = UserSerializerForComment()

    class Meta:
        model = Comment
        fields = (
            'id',
            'tweet_id',
            'user',
            'content',
            'created_at',
            'updated_at',
        )


class CommentSerializerForCreate(serializers.ModelSerializer):
    # 这两项必须手动添加
    # 因为默认 ModelSerializer里只会包含user和tweet而不是user_id 和tweet_id
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('content', 'tweet_id', 'user_id')

    def validate(self, data):
        tweet_id = data['tweet_id']
        if not Tweet.objects.filter(id=tweet_id).exists():
            raise ValidationError({'message': 'tweet does not exist'})
        # 必须 return validated data
        # 也就是验证过之后的， 进行过处理的（当然也可以不做处理） 输入数据
        return data

    def create(self, validated_data):
        return Comment.objects.create(
            user_id=validated_data['user_id'],
            tweet_id=validated_data['tweet_id'],
            content=validated_data['content'],
        )


class CommentSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', )

    def update(self, instance, validated_data):
        instance.content = validated_data['content']
        # 由于懒加载的关系 只有save后才能成功创建实例
        instance.save()
        # update 方法要求 return 修改后的instance 作为返回值
        return instance
