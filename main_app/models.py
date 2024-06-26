from django.db import models
from django.contrib.auth.models import User

CHOICES = (
    ('T', 'Tech'),
    ('C', 'Carpentry'),
    ('R', 'Renovations'),
    ('A', 'Art & Design'),
    ('J', 'Jewelery'),
    ('H', 'Homegoods')
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    profile_pic = models.CharField(max_length=3000, null=True, blank=True)
    bio = models.TextField(max_length=250)

    def __str__(self):
        return self.username


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=250)
    project_type = models.CharField(
        choices=CHOICES, default=CHOICES[0][0], max_length=1)
    # project_img = models.ImageField(
    #     upload_to=upload_to, null=True, blank=True)
    project_img = models.CharField(max_length=250)
    body = models.TextField(max_length=2000)
    link = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_title


class Follow(models.Model):
    following = models.ForeignKey(
        UserProfile, related_name='followers', on_delete=models.CASCADE)
    followers = models.ForeignKey(
        UserProfile, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.following.username) + ' is following ' + str(self.followers.username)


class Favorite(models.Model):
    projects = models.ForeignKey(
        Project, related_name='favorites', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(
        UserProfile, related_name='favorites', on_delete=models.CASCADE)

    def __str__(self):
        return 'Favorites: ' + str(self.user_profile) + ' ' + str(self.projects)


class Comment(models.Model):
    projects = models.ForeignKey(
        Project, related_name="comments", on_delete=models.CASCADE)
    user_profiles = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)
