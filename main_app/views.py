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

# User Registration


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })

# User Login


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)  # Fetch user profile
        refresh = RefreshToken.for_user(
            request.user)  # Generate new refresh token
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class UserProfileList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # This ensures we only return cats belonging to the logged-in user
        user = self.request.user
        return UserProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        # This associates the newly created cat with the logged-in user
        serializer.save(user=self.request.user)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        projects_not_associated = Project.objects.exclude(
            id__in=instance.projects.all())
        projects_serializer = ProjectSerializer(
            projects_not_associated, many=True)

        return Response({
            'UserProfile': serializer.data,
            'projects_not_associated': projects_serializer.data
        })

    def perform_update(self, serializer):
        UserProfile = self.get_object()
        if UserProfile.user != self.request.user:
            raise PermissionDenied(
                {"message": "You do not have permission to edit this project."})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied(
                {"message": "You do not have permission to delete this project."})
        instance.delete()


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'user_profile'


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AddCommentToProject(APIView):
    def post(self, request, project_id, comment_id):
        project = Project.objects.get(id=project_id)
        comment = Comment.objects.get(id=comment_id)
        project.comments.add(comment)
        return Response({'message': f'Comment has been added to Project {project.project_title}'})


class RemoveCommentFromProject(APIView):
    def post(self, request, project_id, comment_id):
        project = Project.objects.get(id=project_id)
        comment = Comment.objects.get(id=comment_id)
        project.comments.remove(comment)
        return Response({'message': f'Comment has been removed from Project {project.project_title}'})
