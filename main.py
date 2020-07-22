###############################################################################
# Author: Orion Crocker
# Filename: main.py
# Date: 01/13/20
# 
# Spotify Collage Creator
#   Automatically downloads all album art from Spotify playlist and assembles a
#     collage
################################################################################

import argparse

from spotify_images import images, collage


def main():

  parse = argparse.ArgumentParser(description='Spotify image gatherer and creator of collages')
  parse.add_argument('-p', '--playlist', dest='playlist', type=str, help='Get all album art from a specific playlist')
  parse.add_argument('-a', '--artist', dest='artist', type=str, help='Get album art from an artist, by default it grabs first 10')
  parse.add_argument('-c', '--collage', action='count', default=0, help='Create a collage out of images gathered from "playlist" or "artist" argument.')
  parse.add_argument('-o', '--output', dest='output', type=str, help='Specify the name of the collage, must have -c flag active to use')
  parse.add_argument('-v', '--verbose', action='count', default=0, help='See the program working instead of just believing that it is working')

  args = parse.parse_args()

  if not args.playlist and not args.artist:
    parse.print_help()
    exit(1)

  if args.playlist and args.artist:
    parse.print_help()
    print("\nCan only do playlist OR artist")
    exit(1)
  
  v = args.verbose
  c = args.collage
  o = args.output

  if not c and o:
    parse.print_help()
    print("\nCannot specify name of collage without -c flag")
    exit(1)

  directory = ''
  if args.playlist:
    directory = images.get_playlist_images(args.playlist, v)
  elif args.artist:
    directory = images.get_artist_images(args.artist, v)

  if c:
    collage.make_collage(filename=o, directory=directory, verbose=v)


if __name__ == '__main__':
  main()
