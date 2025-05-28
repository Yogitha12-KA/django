
from django.contrib.auth.models import User # type: ignore
from django.db import models # type: ignore



class Artwork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='artworks/')
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks')
    likes = models.ManyToManyField(User, related_name='liked_artworks', blank=True)

    def total_likes(self):
        return self.likes.count()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.artist.username}"
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artwork')  # Prevent duplicate likes
class Comment(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)


class Like(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
