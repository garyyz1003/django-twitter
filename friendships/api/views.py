from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from friendships.models import Friendship
from friendships.api.serializers import (
    FollowerSerializer,
    FollowingSerializer,
    FriendshipSerializerForCreate,
)

from django.contrib.auth.models import User


# 让viewset 显示需要有三个步骤：
# 1. 将该package 加入到setting的install中
# 2. 将该viewset 加入到urls的router.register中
# 3. 给该viewset写一个list方法
class FriendshipViewSet(viewsets.GenericViewSet):
    # 如果有需要使用POST的方法则需要定义serializer_class
    # 在调用POST的方法时， 程序会去寻找serializer
    serializer_class = FriendshipSerializerForCreate
    queryset = User.objects.all()

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    # pk 是primary key
    # 查询用户 pk 的followers
    def followers(self, request, pk):
        # GET /api/friendships/1/followers/
        friendships = Friendship.objects.filter(to_user_id=pk).order_by('-created_at')
        serializer = FollowerSerializer(friendships, many=True)
        return Response(
            {"followers": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followings(self, request, pk):
        # GET /api/friendships/1/followings/
        friendships = Friendship.objects.filter(from_user_id=pk).order_by('-created_at')
        serializer = FollowingSerializer(friendships, many=True)
        return Response(
            {"followings": serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        # /api/friendships/<pk>/follow

        # get_object会检测是否有pk对应的用户，如果没有就会报错
        # 这里也能起到检测要follow的用户是否存在的效果
        # 若不存在会返回404
        self.get_object()
        serializer = FriendshipSerializerForCreate(data={
            'from_user_id': request.user.id,
            'to_user_id': pk,
        })

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        # 此处也可将该serializer存为一个instance
        # instance = serializer.save()
        # 之后在Response中 如此调用：
        # Response(FollowingSerializer(instance).data, status=status.HTTP_201_CREATED)

        # serializer.save()
        # return Response({'success': True}, status=status.HTTP_201_CREATED)
        instance = serializer.save()
        return Response(FollowingSerializer(instance).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        # raise 404 if No user with id=pk
        # self.get_object()
        # 注意pk的类型是str 如果要跟id比较的话主要做类型转换
        # 或者可以在上一行中取出unfollow_user
        unfollow_usr = self.get_object()
        # if request.user.id == unfollow_user.id 这样来比较
        # 或者 用int(pk)
        if request.user.id ==  unfollow_usr.id:
            return Response({
                'Success': False,
                'message': 'You can not unfollow yourself',
            }, status=status.HTTP_400_BAD_REQUEST)
        # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#delete
        # Queryset 的 delete 操作返回两个值，一个是删了多少数据，一个是具体每种类型删了多少
        # 为什么会出现多种类型数据的删除？因为可能因为 foreign key 设置了 cascade 出现级联
        # 删除，也就是比如 A model 的某个属性是 B model 的 foreign key，并且设置了
        # on_delete=models.CASCADE, 那么当 B 的某个数据被删除的时候，A 中的关联也会被删除。
        # 所以 CASCADE 是很危险的，我们一般最好不要用，而是用 on_delete=models.SET_NULL
        # 取而代之，这样至少可以避免误删除操作带来的多米诺效应。
        deleted, _ = Friendship.objects.filter(
            from_user=request.user,
            to_user=unfollow_usr,
        ).delete()
        return Response({'success': True, 'deleted': deleted})

        # MYSQL
        # 工程上不用JOIN 会导致量级变大 效率变低
        # 不要有cascade 导致级联删除
        # drop foreign key constraint

    def list(self, request):
        return Response({"message": "This is a friendship home page"})
        # if 'from_user_id' not in request.query_params and 'to_user_id' not in request.query_params:
        #     return Response('missing from or to user_id', status=400)
        #
        # if 'from_user_id' in request.query_params:
        #     followers = Friendship.objects.filter(
        #         from_user_id=request.query_params['from_user_id']
        #     ).order_by('-created_at')
        #
        #     serializer = FollowerSerializer(followers, many=True)
        #     return Response(
        #         {"followers": serializer.data},
        #         status=status.HTTP_200_OK,
        #     )
        # if 'to_user_id' in request.query_params:
        #     followings = Friendship.objects.filter(
        #         to_user_id=request.query_params['to_user_id']
        #     ).order_by('-created_at')
        #
        #     serializer = FollowingSerializer(followings, many=True)
        #     return Response(
        #         {"followings": serializer.data},
        #         status=status.HTTP_200_OK,
        #     )

