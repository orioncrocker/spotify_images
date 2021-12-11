################################################################################
# Author: Orion Crocker
# Filename: api.py
# Date: 11/13/20
# 
# Spotify API wrapper
#   Returns Spotify api client if configured correctly / connection to server
################################################################################

import config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_access():
  auth = SpotifyClientCredentials(
    client_id=config.client_id,
    client_secret=config.client_secret)
  sp = spotipy.Spotify(auth_manager = auth)
  return sp


def get_artist(url):
  spotify = get_access()
  return spotify.artist_albums(artist_id=url, limit=50)


def get_playlist(url):
  spotify = get_access()
  return spotify.playlist(url, fields='name,tracks.items.track.album.name,tracks.items.track.album.images', market='US')

