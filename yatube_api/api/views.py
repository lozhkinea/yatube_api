from django.shortcuts import get_object_or_404
from posts.models import Follow, Group, Post, User
from rest_framework import exceptions, filters, viewsets
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
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]


class FollowViewSet(viewsets.ModelViewSet):
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
        if "following" not in self.request.data:
            raise exceptions.ValidationError()
        following = get_object_or_404(
            User, username=self.request.data["following"]
        )
        if Follow.objects.filter(
            user=self.request.user, following=following
        ).exists():
            raise exceptions.ValidationError()
        if self.request.user.id == following.id:
            raise exceptions.ValidationError()
        serializer.save(user=self.request.user, following=following)
