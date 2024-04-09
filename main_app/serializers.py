from rest_framework import serializers
from .models import UserProfile, Project, Follow, Favorite, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # Add a password field, make it write-only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def __str__(self):
        return Project.project_title


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True)  # Make the user field read-only

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __str__(self):
        return self.username


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['followers', 'following']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user_profile', 'projects']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user_profile', 'comment_body', 'projects']
