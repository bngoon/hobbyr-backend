from django.db import models
from datetime import date
from django.contrib.auth.model import User

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
    user_profile_id = models.OneToOneField(User, on_delete=models.CASCADE)
    Username = models.CharField(max_length=50)
    profile_pic = models.CharField(max_length=1000)
    bio = models.TextField(max_length=250)


class Project(models.Model):
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=250)
    project_type = models.CharField(choices=CHOICES, default=CHOICES[0][0])
    project_img = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    link = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_title


class Follow(models.Model):
    following = models.ManyToManyField(UserProfile, on_delete=models.CASCADE)
    followers = models.ManyToManyField(UserProfile, on_delete=models.CASCADE)


class Favorite(models.Model):
    project_id = models.ManyToManyField(Project, on_delete=models.CASCADE)
    user_profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Comment(models.Model):
    project_id = models.ManyToManyField(Project, on_delete=models.CASCADE)
    user_profile_id = models.ManyToManyField(
        UserProfile, on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at
