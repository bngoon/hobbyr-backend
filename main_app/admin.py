from django.contrib import admin
from .models import Project, UserProfile, Comment, Favorite, Follow

# Register your models here.
admin.site.register(Project)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Follow)
