from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'gallery'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.frontpage, name='frontpage'),
    path('', views.gallery_view, name='gallery'),
    path('upload/', views.upload, name='upload'),
    path('registration/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('registration/signup/', views.signup_view, name='signup'),
    path('registration/logout/', auth_views.LogoutView.as_view(next_page='gallery:frontpage'), name='logout'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('profile/', views.profile_view, name='profile'),
    path('upload/', views.upload_artwork, name='upload'),
    path('artwork/<int:pk>/', views.artwork_detail, name='artwork_detail'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('artwork/<int:artwork_id>/comment/', views.comment_artwork, name='comment_artwork'),
    path('artwork/<int:artwork_id>/like/', views.like_artwork, name='like_artwork'),
    path('profile/<str:username>/follow/', views.follow_artist, name='follow_artist'),

]
