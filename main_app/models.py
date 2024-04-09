from django.db import models
from django.contrib.auth.models import User

CHOICES = (
    ('T', 'Tech'),
    ('C', 'Carpentry'),
    ('R', 'Renovations'),
    ('P', 'Plumbing'),
    ('A', 'Art & Design'),
    ('L', 'Landscaping'),
    ('J', 'Jewelery'),
    ('H', 'Homegoods')
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    profile_pic = models.CharField(max_length=1000, null=True, blank=True)
    bio = models.TextField(max_length=250)

    def __str__(self):
        return self.username


class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=250)
    project_type = models.CharField(
        choices=CHOICES, default=CHOICES[0][0], max_length=1)
    project_img = models.ImageField(upload_to='projects/')
    body = models.TextField(max_length=1000)
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


class Favorite(models.Model):
    projects = models.ManyToManyField(Project)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Comment(models.Model):
    projects = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_profiles = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)
