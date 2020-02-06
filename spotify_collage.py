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
import os               # create directory if needed
import spotipy          # spotify api
import spotipy.oauth2 as oauth2
import requests         # save https links
from PIL import Image   # work with images
import math
import numpy
import glob

credentials = oauth2.SpotifyClientCredentials(
        client_id=config.client_id,
        client_secret=config.client_secret)

def make_collage(directory, verbose):

  pics = glob.glob(directory + '/*.jpeg')
  pics = [Image.open(i) for i in pics]

  if verbose:
    print("Total unique pictures: " + str(len(pics)))

  grid_size = math.sqrt(len(pics))

  rows = 0
  cols = 0

  if grid_size.is_integer():
    rows, cols = (grid_size, grid_size)
  else:
    grid_size = int(grid_size)
    rows, cols = (grid_size, grid_size+1)

  # hacky adjusting
  if ((rows * cols) > len(pics)):
    cols = cols - 1

  print("Rows: " + str(rows) + "\tCols: " + str(cols))

  counter = 0

  collage = Image.new('RGB', (640 * cols, 640 * rows))
  y_offset = 0

  count = 0;
  
  for row in range (0, rows):
    # create new image the size of one row
    new_row = Image.new('RGB', (640 * cols, 640))
    x_offset = 0

    for col in range (0, cols):
      new_row.paste(pics[count], (x_offset,0))
      count += 1
      x_offset += 640

    # paste row into finished product
    collage.paste(new_row, (0,y_offset))
    y_offset += 640
    
  filename = (directory + '.jpeg').lower()
  collage.save(filename)
  print("Collage saved as: " + filename)

def get_images(uri, verbose):

  token = credentials.get_access_token()
  sp = spotipy.Spotify(auth=token)

  results = sp.playlist(uri, fields='name,tracks.items.track.album.name,tracks.items.track.album.images', market='US')
  
  # get name of playlist for file output
  directory = results['name'].replace(' ','_').replace('/','_')
  if not os.path.exists(directory):
    os.makedirs(directory)

  results = results['tracks']
  results = results['items']

  count = 0
  pics = []
  for track in results:
    url = track['track']['album']['images'][0]['url']
    name = (track['track']['album']['name']).replace(' ','_').replace('/','_').lower()

    if verbose:
      print(name + "\t" + url)
    pic = requests.get(url, allow_redirects=True)

    path = directory + '/' + name + '.jpeg'

    if verbose:
      print(path)

    open(path, 'wb').write(pic.content)
    count += 1
    pics.append(pic)

  return directory

def main():

  parse = argparse.ArgumentParser(description='Spotify Playlist Collage Generator')
  parse.add_argument('-p', '--playlist', dest='playlist', type=str, help='Get all album art from a specific playlist')
  parse.add_argument('-a', '--artist', dest='artist', type=str, help='Get album art from an artist, by default it grabs first 10')
  parse.add_argument('-v', '--verbose', action='count', default=0, help='See the program working or just believe that it is working')

  args = parse.parse_args()

  if not args.playlist:
    parse.print_help()
    exit(1)

  v = args.verbose

  directory = get_images(args.playlist, v)
  make_collage(directory, v)

if __name__ == '__main__':
  main()
