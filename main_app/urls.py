from django.urls import path
from .views import Home, FavoriteList, FollowerList, CreateUserView, LoginView, VerifyUserView, ProjectList, ProjectDetail, UserProfileList, UserProfileDetail, CommentList, AddCommentToProject, RemoveCommentFromProject, AddProjectToFavorite, RemoveProjectFromFavorite, AddFollowerToUserProfile, RemoveFollowerFromUserProfile

urlpatterns = [
    path('', Home.as_view(), name='home'),

    # User paths
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),


    # Project Paths
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<int:id>/', ProjectDetail.as_view(), name='project-detail'),
    # Profile Paths
    path('profiles/', UserProfileList.as_view(), name='profile-list'),
    path('profiles/<int:id>/', UserProfileDetail.as_view(), name='profile-detal'),
    # Comment Paths
    path('comments/', CommentList.as_view(), name='comment'),
    path('projects/<int:project_id>/add_comment/<int:comment_id>/',
         AddCommentToProject.as_view(), name='add-comment'),
    path('projects/<int:project_id>/remove_comment/<int:comment_id>/',
         RemoveCommentFromProject.as_view(), name='remove-comment'),


    path('followers/', FollowerList.as_view(), name='followers'),
    path('userprofiles/<int:userprofile_id>/add_follower/<int:follower_id>/',
         AddFollowerToUserProfile.as_view(), name='add-follower'),
    path('userprofiles/<int:userprofile_id>/remove_follower/<int:follower_id>/',
         RemoveFollowerFromUserProfile.as_view(), name='remove-follower'),

    path('favorites/', FavoriteList.as_view(), name='favorites'),
    path('projects/<int:project_id>/add_favorites/<int:favorite_id>/',
         AddProjectToFavorite.as_view(), name='add-favorite'),
    path('projects/<int:project_id>/remove_favorites/<int:favorite_id>/',
         RemoveProjectFromFavorite.as_view(), name='remove-favorite'),









]
