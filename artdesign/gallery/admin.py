
from django.contrib import admin
from .models import Artwork, Like, Comment, Follow

admin.site.register(Artwork)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
