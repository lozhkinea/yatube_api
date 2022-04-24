from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post, User
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api import serializers
from api.permissions import IsAuthorOrReadOnly, IsFollower


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        serializer.save(author=self.request.user, post_id=post_id)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class FollowViewSet(CreateListViewSet):
    queryset = Follow.objects.all()
    serializer_class = serializers.FollowSerializer
    permission_classes = [
        IsFollower,
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        following = get_object_or_404(
            User, username=self.request.data["following"]
        )
        serializer.save(user=self.request.user, following=following)
