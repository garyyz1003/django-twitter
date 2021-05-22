from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
)


class CommentViewSet(viewsets.GenericViewSet):
    """
    只实现 list， create， update， destroy 的方法
    不实现 retrieve （查询单个Comment） 的方法， 因为没这个需求
    """
    # serializer_class 的作用是在django framework界面UI测试的时候基于哪个Serializer去渲染、显示表单
    serializer_class = CommentSerializerForCreate
    # queryset 不是必须要加，但是如果需要用到基于queryset的函数时则需要声明， 例如get_object
    queryset = Comment.objects.all()

    # 已经被实现好的方法 如果要更改的话就是重写该方法
    # POST /api/comments/ -> create
    # GET /api/comments/ -> list
    # GET  /api/comments/1/ -> retrieve
    # DELETE /api/comments/1/ -> destroy
    # PATCH /api/comments/1/ -> partial_update
    # PUT /api/comments/1/ -> update

    # 此处也是对已有函数重写
    def get_permissions(self):
        # 注意要加用（）
        # 不然的话只是一个类名 而不是创建一个实例
        if self.action == 'create':
            return [IsAuthenticated()]
        return [AllowAny()]

    # def list(self, request):
    #     pass

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
                'message': 'Please check input'
            }, status=status.HTTP_400_BAD_REQUEST)

        # save 方法会触发serializer 里的create 方法， 点进 save的具体实现里可以看到
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    # def update(self, request):
    #     pass
    #
    # def destroy(self):
    #     pass
