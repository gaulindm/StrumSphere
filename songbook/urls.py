from django.urls import path
from songbook import views
from .views import (
    SongListView,
    SongCreateView,
    SongUpdateView,
    SongDeleteView,
    UserSongListView,
    ScoreView,
    ArtistListView,
    edit_song_formatting
)

from .views import preview_pdf

#from users.views import update_preferences  # Ensure this import is correct!


urlpatterns = [
    # 🔹 Homepages for each site
    #path('FrancoUke/', home, {'site_name': 'FrancoUke'}, name='francouke_home'),
    #path('StrumSphere/', home, {'site_name': 'StrumSphere'}, name='strumsphere_home'),
    path('', SongListView.as_view(), name='songbook-home'),

    # 🔹 Song List for Each Site
    path('FrancoUke/songs/', SongListView.as_view(), {'site_name': 'FrancoUke'}, name='francouke_songs'),
    path('StrumSphere/songs/', SongListView.as_view(), {'site_name': 'StrumSphere'}, name='strumsphere_songs'),

    # 🔹 User-Specific Songs (Contributed by User)
    path('FrancoUke/user/<str:username>/', UserSongListView.as_view(), {'site_name': 'FrancoUke'}, name='francouke_user_songs'),
    path('StrumSphere/user/<str:username>/', UserSongListView.as_view(), {'site_name': 'StrumSphere'}, name='strumsphere_user_songs'),

    # 🔹 Individual Song View (Score)
    path('FrancoUke/song/<int:pk>/', ScoreView.as_view(), {'site_name': 'FrancoUke'}, name='francouke_score'),
    path('StrumSphere/song/<int:pk>/', ScoreView.as_view(), {'site_name': 'StrumSphere'}, name='strumsphere_score'),

    # 🔹 Song Creation, Update, and Deletion
    path('song/new/', SongCreateView.as_view(), name='song-create'),
    path('song/<int:pk>/update/', SongUpdateView.as_view(), name='song-update'),
    path('song/<int:pk>/delete/', SongDeleteView.as_view(), name='song-delete'),

    # 🔹 PDF Generation
    path("preview_pdf/<int:song_id>/", preview_pdf, name="preview_pdf"),
    path('generate-song-pdf/<int:song_id>/', views.generate_single_song_pdf, name='generate_single_song_pdf'),

    path('generate_multi_song_pdf/', views.generate_multi_song_pdf, name='generate_multi_song_pdf'),

    # 🔹 Artists (Filtering should be site-specific)
    path('FrancoUke/artists/', ArtistListView.as_view(), {'site_name': 'FrancoUke'}, name='francouke_artist_list'),
    path('StrumSphere/artists/', ArtistListView.as_view(), {'site_name': 'StrumSphere'}, name='strumsphere_artist_list'),

    path('FrancoUke/artists/letter/<str:letter>/', ArtistListView.as_view(), {'site_name': 'FrancoUke'}, name='francouke_artist_by_letter'),
    path('StrumSphere/artists/letter/<str:letter>/', ArtistListView.as_view(), {'site_name': 'StrumSphere'}, name='strumsphere_artist_by_letter'),

    path('FrancoUke/artists/<str:artist_name>/', SongListView.as_view(), {'site_name': 'FrancoUke'}, name='francouke_artist_songs'),
    path('StrumSphere/artists/<str:artist_name>/', SongListView.as_view(), {'site_name': 'StrumSphere'}, name='strumsphere_artist_songs'),

    # 🔹 Chord Dictionary
    path('chord-dictionary/', views.chord_dictionary, name='chord-dictionary'),

    # 🔹 Formatting Editor
    path("songs/<int:song_id>/edit_formatting/", edit_song_formatting, name="edit_formatting"),

    # 🔹 Static Pages
    path('about/', views.about, name='songbook-about'),
    path('betabugs/', views.betabugs, name='songbook-betabugs'),
]
