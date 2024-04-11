from django.urls import path, include
from rest_framework import routers
from .views import Home, ProjectTypeList, ProjectByProfile, FollowerList, CreateUserView, LoginView, VerifyUserView, ProjectList, ProjectDetail, UserProfileList, UserProfileDetail, CommentList, AddCommentToProject, CommentDetails, FavoriteViewSet, FollowUser, UnfollowUser, FollowersView

favorite_router = routers.DefaultRouter()
favorite_router.register(r'favorite', FavoriteViewSet)

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
    # add comment
    path('projects/<int:project_id>/add_comment/',
         AddCommentToProject.as_view(), name='add-comment'),
    # remove comment by id
    path('comments/<int:id>/',
         CommentDetails.as_view(), name='comment-details'),


    path('followers/', FollowerList.as_view(), name='followers'),
    path('followers/<int:userprofile_id>/',
         FollowersView.as_view(), name='followers'),
    # followers paths
    path('follow/<int:userprofile_id>/',
         FollowUser.as_view(), name='follow_user'),
    # unfollow path
    path('unfollow/<int:userprofile_id>/',
         UnfollowUser.as_view(), name='unfollow_user'),

     path('projects/type/<str:project_type>/', ProjectTypeList.as_view(), name='projects-by-type'),
     path('projects/user-profile/<int:user_profile_id>/', ProjectByProfile.as_view(), name='projects-by-user-profile'),

    # Favorites
    path('', include(favorite_router.urls)),

    #     path('projects/<int:project_id>/add_favorites/<int:favorite_id>/',
    #          AddProjectToFavorite.as_view(), name='add-favorite'),
    #     path('projects/<int:project_id>/remove_favorites/<int:favorite_id>/',
    #          RemoveProjectFromFavorite.as_view(), name='remove-favorite'),


]
