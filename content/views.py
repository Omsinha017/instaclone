from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (UserPostCreateSerializer, 
                          PostMediaCreateSerializer, 
                          PostFeedSerializer, 
                          PostLikeCreateSerializer,
                          PostCommentCreateSerializer)
from .models import PostMedia, UserPost, PostLikes, PostComments
from .filters import CurrentUserFollowingFilterBackend
from .permissions import IsOwnerOrReadOnly

class UserPostCreateFeed(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         generics.GenericAPIView):

    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [CurrentUserFollowingFilterBackend, ]

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostFeedSerializer
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request['from_user'] = request.user.profile.id
        return self.create(request, *args, **kwargs)

class PostMediaView(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         generics.GenericAPIView):

    queryset = PostMedia.objects.all()
    serializer_class = PostMediaCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserPostDeatilUpdateView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            generics.GenericAPIView):

    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostFeedSerializer
        return self.serializer_class

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class PostLikeViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PostLikes.objects.all()
    serializer_class = PostLikeCreateSerializer


    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}
    
    def list(self, request):

        post_likes = self.queryset.filter(post_id=request.query_params['post_id'])

        page = self.paginate_queryset(post_likes)

        if page:
            serializer = self.get_serializer(post_likes, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(post_likes, many=True)
        return Response(serializer.data)
    
class PostCommentViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = PostComments.objects.all()
    serializer_class = PostCommentCreateSerializer

    def get_serializer_context(self):
        return {'current_user': self.request.user.profile}
    
    def list(self, request):

        post_comments = self.queryset.filter(post_id=request.query_params['post_id'])

        page = self.paginate_queryset(post_comments)

        if page:
            serializer = self.get_serializer(post_comments, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(post_comments, many=True)
        return Response(serializer.data)