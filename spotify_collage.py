################################################################################
# Author: Orion Crocker
# Filename: spotify_collage.py
# Date: 01/13/20
# 
# Spotify Collage Creator
#   Automatically downloads all album art from Spotify playlist and assembles a
#     collage
################################################################################

import config           # credentials
import argparse         # parsing arguments
import os               # save file location
import spotipy          # spotify api
import spotipy.oauth2 as oauth2
import requests         # save https links
from PIL import Image   # work with images

credentials = oauth2.SpotifyClientCredentials(
        client_id=config.client_id,
        client_secret=config.client_secret)

def get_images(uri):

  token = credentials.get_access_token()
  sp = spotipy.Spotify(auth=token)

  results = sp.playlist(uri, fields='name,tracks.items.track.album.images', market='US')
  
  # get name of playlist for file output
  name = results['name']
  name = name.replace(' ','_')

  results = results['tracks']
  results = results['items']

  count = 0
  pics = []
  for track in results:
    url = track['track']['album']['images'][0]['url']
    print(url)
    pic = requests.get(url, allow_redirects=True)
    count += 1
    pics.append(pic)
  return len(pics)

def main():

  parse = argparse.ArgumentParser(description='Spotify Playlist Collage Generator')
  parse.add_argument('-p', '--playlist', dest='playlist', type=str, help='create collage of playlist album art')

  args = parse.parse_args()

  if not args.playlist:
    parse.print_help()
    exit(1)

  count = get_images(args.playlist)
  print(str(count) + " pictures downloaded.")

if __name__ == '__main__':
  main()
