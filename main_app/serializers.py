from rest_framework import serializers
from datetime import datetime
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
    project_img = serializers.ImageField(required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def __str__(self):
        return Project.project_title


class UserProfileSerializer(serializers.ModelSerializer):
    # Fetch username from user relation
    username = serializers.CharField(
        source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    user_profiles = UserProfileSerializer(
        read_only=True)
    # Nested UserProfileSerializer
    formatted_created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # Include the nested UserProfileSerializer field
        fields = ['id', 'comment_body',
                  'user_profiles', 'formatted_created_at']

    def create(self, validated_data):
        # This is called when a new Comment instance is created via the API
        # Here you need to handle creation of comments correctly if user_profile is not included in the incoming request
        return Comment.objects.create(**validated_data)

    def get_formatted_created_at(self, obj):
        # Format as 'Month day, Year, HH:MM AM/PM'
        return obj.created_at.strftime('%B %d, %Y, %I:%M %p')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['followers', 'following', 'followers']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user_profile', 'projects',]
