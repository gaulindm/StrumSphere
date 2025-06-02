# models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import re
import json
from .parsers import parse_song_data  # Import the parse_song_data function
from .utils.transposer import detect_key
from taggit.managers import TaggableManager
from django.conf import settings

class Song(models.Model):
    SITE_CHOICES = [
        ('FrancoUke', 'FrancoUke'),
        ('StrumSphere', 'StrumSphere'),
    ]

    songTitle = models.CharField(max_length=100, blank=True, null=True)
    songChordPro = models.TextField()  # Original
    lyrics_with_chords = models.JSONField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    metadata = models.JSONField(blank=True, null=True)  # Stores metadata as JSON
    date_posted = models.DateField(default=timezone.now)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    acknowledgement = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.CharField(max_length=20, choices=SITE_CHOICES, default='FrancoUke')  # NEW FIELD

    def save(self, *args, **kwargs):
        # Check if the song exists and retrieve old data
        if self.pk:
            old_song = Song.objects.get(pk=self.pk)
            if old_song.songChordPro != self.songChordPro:
                self.date_posted = timezone.now().date()  # Update date_posted when content changes

        # Only parse title if songTitle is not manually set
        if not self.songTitle:
            self.songTitle, self.metadata = self.parse_metadata_from_chordpro()
        else:
            # Only update metadata
            _, self.metadata = self.parse_metadata_from_chordpro()

        # Parse the songChordPro content of the song
        self.lyrics_with_chords = parse_song_data(self.songChordPro)

        super().save(*args, **kwargs)

    def parse_metadata_from_chordpro(self):
        tags = {
            "title": re.search(r'{(?:title|t):\s*([^\}]+)}', self.songChordPro, re.IGNORECASE | re.UNICODE),
            "comment": re.search(r'{(?:comment|c):\s*(.+?)}', self.songChordPro, re.IGNORECASE | re.UNICODE),
            "artist": re.search(r'{artist:\s*([^\}]+)}', self.songChordPro, re.IGNORECASE | re.UNICODE),
            "songwriter": re.search(r'{songwriter:\s*([^\}]+)}', self.songChordPro, re.IGNORECASE | re.UNICODE),
            "capo": re.search(r'{capo:\s*([^\}]+)}', self.songChordPro, re.IGNORECASE | re.UNICODE),
            "album": re.search(r'{album:\s*(.+?)}', self.songChordPro, re.IGNORECASE | re.UNICODE),
            "year": re.search(r'{year:\s*(\d{4})}', self.songChordPro, re.IGNORECASE),
            "key": re.search(r'{key:\s*(.+?)}', self.songChordPro, re.IGNORECASE),
            "1stnote": re.search(r'{1stnote:\s*(.+?)}', self.songChordPro, re.IGNORECASE),
            "tempo": re.search(r'{tempo:\s*(.+?)}', self.songChordPro, re.IGNORECASE),
            "timeSignature": re.search(r'{timeSignature:\s*(.+?)}', self.songChordPro, re.IGNORECASE),
            "youtube": re.search(r'{youtube:\s*(https?://[^\s\}]+)}', self.songChordPro, re.IGNORECASE),  
        }

        metadata = {tag: match.group(1) if match else None for tag, match in tags.items()}
        title = metadata.pop("title", "Untitled Song")

        return title, metadata

    def __str__(self):
        return f"{self.songTitle} ({self.site_name})" if self.songTitle else f"Untitled Song ({self.site_name})"

    def get_absolute_url(self):
        return reverse('score', kwargs={'pk': self.pk})

    def get_used_chords(self):
        def flatten_lyrics(lyrics):
            flat_list = []
            for item in lyrics:
                if isinstance(item, list):
                    flat_list.extend(flatten_lyrics(item))
                elif isinstance(item, str):
                    flat_list.append(item)
            return flat_list

        if isinstance(self.lyrics_with_chords, list):
            flat_lyrics = flatten_lyrics(self.lyrics_with_chords)
            lyrics_text = '\n'.join(flat_lyrics)
        else:
            lyrics_text = str(self.lyrics_with_chords)

        return list(set(re.findall(r'\[([A-G][#b]?(maj|min|dim|aug|sus|6|7|9)?)\]', lyrics_text)))

class SongFormatting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)  # Link to the song

    # Store formatting settings for each section as JSON
    intro = models.JSONField(default=dict, blank=True)
    verse = models.JSONField(default=dict, blank=True)
    chorus = models.JSONField(default=dict, blank=True)
    bridge = models.JSONField(default=dict, blank=True)
    interlude = models.JSONField(default=dict, blank=True)
    outro = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('user', 'song')  # Ensure each user has only one formatting per song

    def __str__(self):
        return f"Formatting for {self.song.songTitle} by {self.user.username}"