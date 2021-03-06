from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from comments.api.permissions import IsObjectOwner
from utils.decorators import required_params


# GenericViewSet如果不定义list方法是不能显示model具体内容的
# 而ModelViewSet 可以， 可以用来方便测试
# GenericSerializer和 ModelSerializer同理
class CommentViewSet(viewsets.GenericViewSet):
    """
    只实现 list， create， update， destroy 的方法
    不实现 retrieve （查询单个Comment） 的方法， 因为没这个需求
    """
    # serializer_class 的作用是在django framework界面UI测试的时候基于哪个Serializer去渲染、显示表单
    serializer_class = CommentSerializerForCreate
    # queryset 不是必须要加，但是如果需要用到基于queryset的函数时则需要声明， 例如get_object
    queryset = Comment.objects.all()
    # 需要实现安装django_filter才能使用
    filterset_fields = ('tweet_id',)

    # 已经被实现好的方法 如果要更改的话就是重写该方法
    # POST /api/comments/ -> create
    # GET /api/comments/ -> list
    # GET  /api/comments/1/ -> retrieve
    # DELETE /api/comments/1/ -> destroy
    # PATCH /api/comments/1/ -> partial_update 基本不用
    # PUT /api/comments/1/ -> update

    # 此处也是对已有函数重写
    def get_permissions(self):
        # 注意要加用（）
        # 不然的话只是一个类名 而不是创建一个实例
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['destroy', 'update']:
            # 虽然只返回IsObjectOwner()功能上也能达到效果，但是提示的错误信息不对，会对用户造成误导
            return [IsAuthenticated(), IsObjectOwner()]
        return [AllowAny()]

    @required_params(params=['tweet_id'])
    def list(self, request, *args, **kwargs):
        # 我们的实现中必须要包含tweet_id， 之前使用如下的方式检验的
        # 因为发现tweet中也要检查user_id 所以我们使用decorator的方式将两个功能相似的步骤简化为一个
        # if 'tweet_id' not in request.query_params:
        #     return Response({
        #         'message': 'missing tweet_id in request',
        #         'success': False,
        #     }, status=status.HTTP_400_BAD_REQUEST,)
        # 全部的comment混在一起是没有什么意义的
        if 'tweet_id' not in request.query_params:
            return Response({
                'message': 'missing tweet_id in request',
                'success': False,
            }, status=status.HTTP_400_BAD_REQUEST,)
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset)\
            .prefetch_related('user')\
            .order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(
            {'comments': serializer.data},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):

        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        # 注意这里必须要加 'data=data' 来指定参数是传给data的
        # 因为默认的第一个参数是instance

        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        # save 方法会触发serializer 里的create 方法， 点进 save的具体实现里可以看到
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        # get_object() 是 DRF 包装的一个函数， 会在找不到的时候raise 404 error
        # 所以这里无需做额外判断
        # 如果不指定instance， 在 new serializer会自动调用create 方法
        # 有了instance就会调用serializer里的update 方法
        serializer = CommentSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        # save 方法会触发 serializer 里的update方法， 点进 save的具体实现里可以看到
        # save 是根据 instance 参数有没有传来决定是触发create 还是 update
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        # 不需要创建serializer
        comment = self.get_object()
        comment.delete()
        # DRF 里默认destroy 返回的是status code = 204 no content
        # 这里return 了 success=True更直观的让前端去做判断， 所以return 200更合适
        return Response({
            'Success': 'True'
        }, status=status.HTTP_200_OK)
