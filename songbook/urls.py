from django.urls import path
from songbook import views
from .views import (
    SongListView, 
    SongCreateView,
    SongUpdateView,
    SongDeleteView,
    UserSongListView,
    ScoreView,
)

from .views import preview_pdf


urlpatterns = [
    path('', SongListView.as_view(), name='songbook-home'),
#    path('', views.song_list, name='song_list'),
    path('user/<str:username>', UserSongListView.as_view(), name='user-songs'),
    path('score/<int:pk>/', ScoreView.as_view(),name='score'),
    path('song/new/', SongCreateView.as_view(), name='song-create'),
    path("preview_pdf/<int:song_id>/", preview_pdf, name="preview_pdf"),
    path('song/<int:pk>/update/', SongUpdateView.as_view(), name='song-update'),
    path('song/<int:pk>/delete/', SongDeleteView.as_view(), name='song-delete'),
    path('about/', views.about, name='songbook-about'),
    path('betabugs/', views.betabugs, name='songbook-betabugs'),
    path('', SongListView.as_view(), name='song_list'),  # Define a name for this pattern
    path('generate-song-pdf/<int:song_id>/', views.generate_single_song_pdf, name='generate_single_song_pdf'),

    path('chord-dictionary/', views.chord_dictionary, name='chord-dictionary'),
    path('generate_titles_pdf/', views.generate_titles_pdf, name='generate_titles_pdf'),
    path('generate_multi_song_pdf/', views.generate_multi_song_pdf, name='generate_multi_song_pdf'),

]
    
