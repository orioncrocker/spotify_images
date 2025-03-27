################################################################################
# Author: Orion Crocker
# Filename: api.py
# Date: 11/13/20
# 
# Spotify API wrapper
#   Returns Spotify api client if configured correctly / connection to server
################################################################################

import config, globals
import json
import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials


def clean_string(string):
  string = string.lower()
  replace = [(' ','_'),('/','_'),('[','('),(']',')')]
  for r,w in replace:
    string =string.replace(r,w)
  return string

def get_api_access():
  auth = SpotifyClientCredentials(
    client_id=config.client_id,
    client_secret=config.client_secret)
  globals.spotify = spotipy.Spotify(auth_manager = auth)

def query_artist_name(url):
  if globals.spotify is None:
    get_api_access()

  results = globals.spotify.artist(url)
  return results["name"]

def query_artist_api(url, limit, offset=0):
  if globals.spotify is None:
    get_api_access()

  urls = []
  results = globals.spotify.artist_albums(url,
                                          limit=limit,
                                          include_groups="album,single",
                                          offset=offset)
  i = offset
  for item in results["items"]:
    name = clean_string(item["name"])
    url = item["images"][0]["url"]
    urls.append((name, url))
    if globals.verbose:
      print("%d %s: %s" % (i, name, url))
    i += 1
  return urls

def query_playlist_name(url):
  if globals.spotify is None:
    get_api_access()

  results = globals.spotify.playlist(url, fields="name")
  return results["name"]

def query_playlist_api(url, limit, offset=0):
  # Only return image URLs, everything else can be dropped
  if globals.spotify is None:
    get_api_access()

  urls = []
  results = globals.spotify.playlist_tracks(url,
                                            limit=limit,
                                            offset=offset)
  if len(results) == 0:
    if globals.verbose:
      print("No results found!")
    return urls

  i = offset
  for item in results["items"]:
    track = item["track"]
    url = track["album"]["images"][0]["url"]
    artist_name = clean_string(track["artists"][0]["name"])
    album_name = clean_string(track["album"]["name"])
    name = artist_name + " - " + album_name

    urls.append((name, url))
    if globals.verbose:
      print("%d %s: %s" % (i, name, url))
    i += 1
  return urls

def get_image_list_and_name(url):
  if 'artist' in url:
    limit = 50
    image_query = query_artist_api
    name_query = query_artist_name
  if 'playlist' in url:
    limit = 100
    image_query = query_playlist_api
    name_query = query_playlist_name

  results = image_query(url, limit)

  # If returned limit, there must be more tracks
  if len(results) == limit:
    must_be_more = True
    passes = 1
    while must_be_more:
      wait_time = 1
      print("Found %d results, waiting %d second(s) before next query..." %
            (len(results), wait_time))
      time.sleep(wait_time)
      offset = limit * passes
      tracks = image_query(url, limit, offset=offset)

      # Add batch to the pile
      results.extend(tracks)

      passes += 1
      if len(tracks) < limit:
        must_be_more = False

  urls_as_set = set(results)
  urls = list(urls_as_set)

  name = name_query(url)
  return urls, name
