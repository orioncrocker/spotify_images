################################################################################
# Author: Orion Crocker
# Filename: images.py
# Date: 02/06/20
# 
# Get Spotify Album Art
# Retrieves album art from Spotify's api
################################################################################

import os
import spotipy
import spotipy.oauth2 as oauth2
import requests

# local files
import config

# global credentials from config.py
credentials = oauth2.SpotifyClientCredentials(
        client_id=config.client_id,
        client_secret=config.client_secret)

def rename(name):
  return name.replace(' ','_').replace('/','_').lower()


def get_artist_images(artist, verbose):
  token = credentials.get_access_token()
  sp = spotipy.Spotify(auth=token)

  results = sp.search(q='artist:'+artist, limit=50, type='album')

  if not results:
    print("Could not find artist...")
    exit(1)

  results = results['albums']
  results = results['items']

  directory = 'results/' + rename(artist)
  if not os.path.exists(directory):
    os.makedirs(directory)

  count = 0
  pics = []
  for album in results:

    url = album['images'][0]['url']
    name = rename(album['name'])

    path = directory + '/' + name + '.jpeg'

    if os.path.exists(path):
      continue

    pic = requests.get(url, allow_redirects=True)

    if verbose:
      print(path)

    open(path, 'wb').write(pic.content)
    count += 1
    pics.append(pic)

  print(str(len(pics)) + " saved to " + directory)
  return directory


def url_to_uri(uri):
  offset = uri.find('playlist')
  return 'spotify:' + uri[offset:].replace('/',':')


def get_playlist_images(uri, verbose):
  if uri[:5] == 'https':
    uri = url_to_uri(uri)
  token = credentials.get_access_token()
  sp = spotipy.Spotify(auth=token)
  results = sp.playlist(uri, fields='name,tracks.items.track.album.name,tracks.items.track.album.images', market='US')

  # get name of playlist for file output
  directory = 'results/' + rename(results['name'])
  if not os.path.exists(directory):
    os.makedirs(directory)

  results = results['tracks']
  results = results['items']

  count = 0
  pics = []
  for track in results:
    url = track['track']['album']['images'][0]['url']
    name = rename(track['track']['album']['name'])

    path = directory + '/' + name + '.jpeg'

    if os.path.exists(path):
      continue

    pic = requests.get(url, allow_redirects=True)

    if verbose:
      print(path)

    open(path, 'wb').write(pic.content)
    count += 1
    pics.append(pic)

  print(str(len(pics)) + " saved to " + directory)
  return directory
