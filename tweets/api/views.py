from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from tweets.api.serializers import \
    TweetSerializer, \
    TweetSerializerForCreate, \
    TweetSerializerWithComments
from rest_framework.response import Response
from tweets.models import Tweet
from newsfeeds.services import NewsFeedService
from utils.decorators import required_params


class TweetViewSet(viewsets.GenericViewSet):
    serializer_class = TweetSerializerForCreate
    queryset = Tweet.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @required_params(params=['user_id'])
    def list(self, request, *args, **kwargs):
        # 之前使用如下的方式检验user_id 的
        # 因为发现comments中也要检查tweet_id 所以我们使用decorator的方式将两个功能相似的步骤简化为一个
        # if 'user_id' not in request.query_params:
        #     return Response('missing user_id', status=400)

        # 此处的搜索需要建立联合索引 来加快搜索速度
        # 需要在tweets -- models -- Tweet中建立联合索引
        tweets = Tweet.objects.filter(
            user_id=request.query_params['user_id']
        ).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)  # many=True说明会返回一个list of dict
        return Response({'tweets': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        # 如果要使用get_object 一定要先定义query_set
        tweet = self.get_object()
        return Response(TweetSerializerWithComments(tweet).data)

    def create(self, request):
        serializer = TweetSerializerForCreate(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            }, status=400)

        # save will trigger create method in TweetSerializerForCreate
        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(tweet).data, status=201)
