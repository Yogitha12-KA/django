
# Create your views here.
from tokenize import Comment
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect


from django.shortcuts import render
from .models import Artwork  # adjust model name if needed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArtworkForm, ArtworkUploadForm

def frontpage(request):
    return render(request, 'gallery/frontpage.html')

@login_required
def gallery_view(request):
    artworks = Artwork.objects.all().select_related('artist')
    artworks = Artwork.objects.all().prefetch_related('likes', 'comments', 'artist')

    for artwork in artworks:
        # Set a custom attribute for whether the user has liked this artwork
        artwork.liked_by_user = artwork.likes.filter(id=request.user.id).exists()
        # Set whether the user follows the artist
        artwork.followed_by_user = artwork.artist.followers.filter(id=request.user.id).exists()
  # optional optimization
    return render(request, 'gallery/gallery.html', {'artworks': artworks})


@login_required
def upload(request):
    if request.method == 'POST':
        form = ArtworkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user
            artwork.save()
            return redirect('gallery:gallery')  # change if your gallery view name differs
    else:
        form = ArtworkUploadForm()
    return render(request, 'gallery/upload.html', {'form': form})

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gallery:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
@login_required

def profile_view(request):
    user = request.user  # Logged-in user
    return render(request, 'gallery/profile.html', {'user': user})

from django.shortcuts import get_object_or_404

def artwork_detail(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    return render(request, 'gallery/artwork_detail.html', {'artwork': artwork})


from .forms import CommentForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


from .models import Artwork, Follow, Like
from django.contrib.auth.decorators import login_required

@login_required
def gallery_view(request):
    artworks = Artwork.objects.all()
    return render(request, 'gallery/gallery.html', {'artworks': artworks})

@login_required
def upload_artwork(request):
    if request.method == 'POST':
        title = request.POST['title']
        image = request.FILES['image']
        description = request.POST['description']
        Artwork.objects.create(title=title, image=image, description=description, artist=request.user)
        return redirect('gallery')
    return render(request, 'gallery/upload.html')

from django.contrib.auth.models import User



@login_required
def follow_user(request, username):
    user_to_follow = User.objects.get(username=username)
    request.user.profile.following.add(user_to_follow.profile)
    return redirect('profile', username=username)

@login_required
def artwork_detail(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    if request.method == 'POST':
        if 'like' in request.POST:
            artwork.likes.add(request.user)
        elif 'comment' in request.POST:
            content = request.POST['content']
            Comment.objects.create(artwork=artwork, user=request.user, content=content)
    return render(request, 'gallery/artwork_detail.html', {'artwork': artwork})

@login_required
def comment_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.artwork = artwork
        comment.save()
        return redirect('comment_artwork', artwork_id=artwork.id)
    return render(request, 'art/comment.html', {'artwork': artwork, 'form': form})


@login_required
def like_artwork(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    like, created = Like.objects.get_or_create(user=request.user, artwork=artwork)
    if not created:
        like.delete()  # Toggle like: if already liked, remove
    return redirect('gallery:gallery')
@login_required
def follow_artist(request, username):
    target_user = get_object_or_404(User, username=username)
    follow_relation, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        follow_relation.delete()
    return redirect('profile', username=username)

