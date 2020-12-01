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
import spotipy.oauth2 as oauth2

def get_access():
  credentials = oauth2.SpotifyClientCredentials(
      client_id=config.client_id,
      client_secret=config.client_secret)

  token = credentials.get_access_token()

  if (token == None):
    print("Could not get Spotify access token")
    exit(1)

  return spotipy.Spotify(auth=token)


def get_artist(url):
  spotify = get_access()
  return spotify.artist_albums(artist_id=url, limit=50)

def get_playlist(url):
  spotify = get_access()
  return spotify.playlist(url, fields='name,tracks.items.track.album.name,tracks.items.track.album.images', market='US')
