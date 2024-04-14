from django.shortcuts import render, get_object_or_404
from .serializers import UserSerializer, UserProfileSerializer, ProjectSerializer, CommentSerializer, FollowSerializer, FavoriteSerializer
from rest_framework import generics, status, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile, Project, Comment, Favorite, Follow
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser


class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the hobbyr home route!'}
        return Response(content)


class ProjectTypeList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        project_type = self.kwargs['project_type']

        return Project.objects.filter(project_type=project_type)


class ProjectByProfile(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        user_profile_id = self.kwargs['user_profile_id']

        return Project.objects.filter(user_profile_id=user_profile_id)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'id'
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        id = self.kwargs['id']

        return UserProfile.objects.filter(id=id)


class AddCommentToProject(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        try:
            project = Project.objects.get(
                pk=project_id)  # Correct variable name
        except Project.DoesNotExist:
            raise NotFound('Project not found')

        user_profiles = request.user.userprofile  # Get the user profile instance
        comment_body = request.data.get('comment_body')

        if not comment_body:
            return Response({'error': 'Comment body is required'}, status=400)

        comment = Comment.objects.create(
            projects=project,  # Correct field name according to the model
            user_profiles=user_profiles,  # Correct field name according to the model
            comment_body=comment_body
        )
        # Serialize user profile info
        return Response({'comment_id': comment.id, 'user_profiles': user_profiles.username})


class CommentsListView(generics.ListAPIView):
    model = Comment
    serializer_class = CommentSerializer
    template_name = 'comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Comment.objects.filter(projects__id=project_id).select_related('user_profiles').order_by('-created_at')


class CommentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        except Comment.DoesNotExist:
            return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        # Check if the authenticated user_profile matches the user_profile associated with the comment
        if self.request.user.userprofile != instance.user_profiles:
            raise PermissionDenied(
                'You do not have permission to delete this comment')

        instance.delete()

    def perform_update(self, serializer):
        # Check if the authenticated user_profile matches the user_profile associated with the comment
        if self.request.user.userprofile != serializer.instance.user_profiles:
            raise PermissionDenied(
                'You do not have permission to update this comment')

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# User Registration
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        userProfile = UserProfile.objects.create(
            user=user, username=user.username)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data,
            'userProfile': UserProfileSerializer(userProfile).data
        })

# User Login


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print("username: ", username, "password: ", password)

        user = authenticate(username=username, password=password)

        if user:
            userProfile = UserProfile.objects.get(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'userProfile': UserProfileSerializer(userProfile).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)  # Fetch user profile
        userProfile = UserProfile.objects.get(user=user)
        refresh = RefreshToken.for_user(
            request.user)  # Generate new refresh token
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'userProfile': UserProfileSerializer(userProfile).data
        })


class UserProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticated
    ]


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    permission_classes = [
        permissions.IsAuthenticated
    ]


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class RemoveCommentFromProject(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, project_id, comment_id):
        project = Project.objects.get(id=project_id)
        comment = Comment.objects.get(id=comment_id)
        project.comments.remove(comment)
        return Response({'message': f'Comment has been removed from Project {project.project_title}'})


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]


# class AddProjectToFavorite(APIView):
#     def post(self, request, project_id, favorite_id):
#         project = Project.objects.get(id=project_id)
#         favorite = Favorite.objects.get(id=favorite_id)
#         project.favorites.add(favorite)
#         return Response({'message': f'Comment has been added to Project {project.project_title}'})


# class RemoveProjectFromFavorite(APIView):
#     def post(self, request, project_id, favorite_id):
#         project = Project.objects.get(id=project_id)
#         favorite = Favorite.objects.get(id=favorite_id)
#         project.favorites.remove(favorite)
#         return Response({'message': f'Comment has been removed from Project {project.project_title}'})

# Followers views
# class FollowsList(generics.ListAPIView):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]
class FollowsList(generics.GenericAPIView):
    # Ensure this serializer can serialize a UserProfile
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, userprofile_id, *args, **kwargs):
        # Adjust this according to how UserProfile is linked to User
        user_profile = get_object_or_404(UserProfile, pk=userprofile_id)

        # Get the profiles that follow the user
        followers_query = Follow.objects.filter(following=user_profile)
        followers = [follow.followers for follow in followers_query]

        # Get the profiles that the user is following
        following_query = Follow.objects.filter(followers=user_profile)
        following = [follow.following for follow in following_query]

        # Serialize the data
        profile_serializer = UserProfileSerializer(followers, many=True)
        following_serializer = UserProfileSerializer(following, many=True)

        return Response({
            'followers': profile_serializer.data,
            'following': following_serializer.data
        })

# Follow User


class FollowUser(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, userprofile_id):
        try:
            user_to_follow = UserProfile.objects.get(pk=userprofile_id)
            # Get the UserProfile of the authenticated user
            user_profile = request.user.userprofile
            follow_instance = Follow.objects.create(
                following=user_profile, followers=user_to_follow)
            return Response({"message": "Successfully followed user", "follow_instance_id": follow_instance.id}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "User to follow does not exist"}, status=status.HTTP_404_NOT_FOUND)


class UnfollowUser(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, userprofile_id):
        try:
            user_to_unfollow = UserProfile.objects.get(pk=userprofile_id)
            # Get the UserProfile of the authenticated user
            user_profile = request.user.userprofile
            # Removing the follow relationship
            Follow.objects.filter(following=user_profile,
                                  followers=user_to_unfollow).delete()
            return Response({"message": "Successfully unfollowed user"}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "User to unfollow does not exist"}, status=status.HTTP_404_NOT_FOUND)


class FollowersView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, userprofile_id):
        try:
            user_profile = UserProfile.objects.get(pk=userprofile_id)
            followers = user_profile.followers.all()
            follower_user_profiles = [follow.following for follow in followers]
            serializer = UserProfileSerializer(
                follower_user_profiles, many=True)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile does not exist"}, status=status.HTTP_404_NOT_FOUND)


class ProjectsByFollowedUsers(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the current user's profile (adjust according to your user profile link setup)
        user_profile = self.request.user.userprofile

        # Find all users followed by the current user
        followed_users = Follow.objects.filter(
            followers=user_profile).values_list('following__id', flat=True)

        print(followed_users)

        # Filter projects where the project's user profile is in the list of followed users
        return Project.objects.filter(user_profile_id__in=followed_users)
