from django.shortcuts import render
from .serializers import UserSerializer, UserProfileSerializer, ProjectSerializer, CommentSerializer, FollowSerializer, FavoriteSerializer
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile, Project, Comment, Favorite, Follow


class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the hobbyr home route!'}
        return Response(content)


class AddCommentToProject(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def add_comment_to_project(request, project_id):
        if request.method == 'POST':
            project = Project.objects.get(pk=project_id)
            user_profile = request.user.userprofile
            comment_body = request.POST.get('comment_body')
            comment = Comment.objects.create(
                project=project, user_profile=user_profile, comment_body=comment_body)
            return Response({'comment_id': comment.id})
        else:
            return Response({'error': 'POST request required'}, status=400)


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


# class AddCommentToProject(APIView):

#     def post(self, request, project_id, comment_id):
#         try:
#             project = Project.objects.get(id=project_id)
#         except Project.DoesNotExist:
#             return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             comment = Comment.objects.create(id=comment_id)
#         except Comment.DoesNotExist:
#             return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

#         project.comments.add(comment)

#         return Response({'message': f'Comment has been added to Project {project.project_title}'})

#     def get_queryset(self):
#         queryset = Comment.objects.all()
#         return queryset

# class AddCommentToProject(generics.CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def perform_create(self, serializer):
#         project_id = self.kwargs.get('project_id')
#         project = Project.objects.get(id=project_id)
#         serializer.save(self.request.user, project=project)


class UserProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'id'
    queryset = UserProfile.objects.all()


# class AddCommentToProject(APIView):
#     def post(self, request, project_id, comment_id):
#         try:
#             project = Project.objects.get(id=project_id)
#         except Project.DoesNotExist:
#             return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

#         try:
#             comment = Comment.objects.get(id=comment_id)
#         except Comment.DoesNotExist:
#             return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Assuming you want to associate the comment with the authenticated user's profile
#         try:
#             user_profiles = UserProfile.objects.get(user=request.user)
#         except UserProfile.DoesNotExist:
#             return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

#         project.comments.add(comment)

#         return Response({'message': f'Comment has been added to Project {project.project_title}'})

    # def get_queryset(self):
    #     user = self.request.user
    #     return UserProfile.objects.filter(user=user)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)

    #     projects_not_associated = Project.objects.exclude(
    #         id__in=instance.projects.all())
    #     projects_serializer = ProjectSerializer(
    #         projects_not_associated, many=True)

    # return Response({
    #     'UserProfile': serializer.data,
    #     'projects_not_associated': projects_serializer.data
    # })

    # def perform_update(self, serializer):
    #     UserProfile = self.get_object()
    #     if UserProfile.user != self.request.user:
    #         raise PermissionDenied(
    #             {"message": "You do not have permission to edit this project."})
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     if instance.user != self.request.user:
    #         raise PermissionDenied(
    #             {"message": "You do not have permission to delete this project."})
    #     instance.delete()


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RemoveCommentFromProject(APIView):
    def post(self, request, project_id, comment_id):
        project = Project.objects.get(id=project_id)
        comment = Comment.objects.get(id=comment_id)
        project.comments.remove(comment)
        return Response({'message': f'Comment has been removed from Project {project.project_title}'})


class FavoriteList(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class AddProjectToFavorite(APIView):
    def post(self, request, project_id, favorite_id):
        project = Project.objects.get(id=project_id)
        favorite = Favorite.objects.get(id=favorite_id)
        project.favorites.add(favorite)
        return Response({'message': f'Comment has been added to Project {project.project_title}'})


class RemoveProjectFromFavorite(APIView):
    def post(self, request, project_id, favorite_id):
        project = Project.objects.get(id=project_id)
        favorite = Favorite.objects.get(id=favorite_id)
        project.favorites.remove(favorite)
        return Response({'message': f'Comment has been removed from Project {project.project_title}'})


class FollowerList(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class AddFollowerToUserProfile(APIView):
    def post(self, request, userprofile_id, follow_id):
        UserProfile = UserProfile.objects.get(id=userprofile_id)
        follow = Follow.objects.get(id=follow_id)
        project.followers.add(follower)
        return Response({'message': f'Comment has been added to Project {project.project_title}'})


class RemoveFollowerFromUserProfile(APIView):
    def post(self, request, userpofile_id, follow_id):
        UserProfile = UserProfile.objects.get(id=userprofile_id)
        follow = Follow.objects.get(id=follow_id)
        project.followers.remove(follower)
        return Response({'message': f'Comment has been removed from Project {project.project_title}'})
