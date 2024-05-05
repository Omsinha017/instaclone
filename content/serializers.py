from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UserPost, PostMedia, PostLikes, PostComments
from users.serializers import UserProfileViewSerializer

class UserPostCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['author'] = self.context['current_user']
        return UserPost.objects.create(**validated_data)

    class Meta:
        model = UserPost
        fields = ('caption_text', 'location', 'id', )

class PostMediaCreateSerializer(ModelSerializer):

    class Meta:
        model = PostMedia
        fields = ('media_file', 'sequence_index', 'post', )


class PostMediaViewSerializer(ModelSerializer):

    class Meta:
        model = PostMedia
        exclude = ('post', )


class PostFeedSerializer(ModelSerializer):

    author = UserProfileViewSerializer()
    media = PostMediaViewSerializer(many=True)

    class Meta:
        model = UserPost
        fields = '__all__'
        include = ('media', )

class PostLikeCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['liked_by'] = self.context['current_user']

        return PostLikes.objects.create(**validated_data)

    class Meta:
        model = PostLikes
        fields = ('id', 'post')
    
class PostCommentCreateSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data['author'] = self.context['current_user']

        return PostComments.objects.create(**validated_data)

    class Meta:
        model = PostComments
        fields = ('id', 'text', 'post', )