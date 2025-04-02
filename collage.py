################################################################################
# Author: Orion Crocker
# Filename: collage.py
# Date: 02/06/20
# 
# Collage Creator
# Creates a collage of images based on directory given
################################################################################

import argparse
import os
import glob
import math
import globals
from PIL import Image

ratio_by_resolution = {
    "4:3":   [(800,600),(1024,768),(1280,960)],
    "16:9":  [(1280,720),(1600,900),(1920,1080),(2560,1440),(3840,2160),(5120,2880),(7680,4320)],
    "16:10": [(1280,800),(1440,900),(1680,1050),(1920,1200),(2560,1600),(3840,2400)],
    "32:9":  [(3840,1080),(5120,1400),(6400,1800),(7680,2160)],
}


def get_closest_resolution(ratio, x_size, y_size):
  resolutions = ratio_by_resolution[ratio]
  closest_x = resolutions[0][0]
  idx = 0
  for x,y in resolutions:
    x1_diff = x_size - closest_x
    x2_diff = x_size - x

    if x2_diff < 0:
      # Resolutions higher than current are disqualified!
      break

    if (x2_diff < x1_diff):
      closest_x = x
      idx += 1

  closest_y = resolutions[idx][1]
  return closest_x, closest_y

def get_wallpaper_ratio():
  x,y = map(int, globals.wallpaper_ratio.split(':'))
  return x/y

def calc_wallpaper_border(rows, cols):
  target_ratio = get_wallpaper_ratio()
  current_ratio = cols/rows
  if globals.verbose:
    print("Target ratio: %f" % target_ratio)

  x_size = globals.image_size * cols
  x_needed = ((x_size * target_ratio) / current_ratio) - x_size
  x_border = math.floor(x_needed / 2)

  # TODO!
  y_border = 0
  return x_border,y_border

def calc_wallpaper_grid(total):
  wallpaper_ratio = get_wallpaper_ratio()

  square = math.ceil(math.sqrt(total))
  closest_ratio = square/square
  final_cols = square
  final_rows = square

  for cols in range(square, square*2):
    rows = square - (cols - square)
    ratio = cols/rows
    wall_diff = wallpaper_ratio - ratio

    if wall_diff < 0:
        closest_ratio = ratio
        final_cols = cols
        final_rows = rows

        if total < (final_cols * final_rows):
          final_cols -= 1
        break;

  return final_rows, final_cols

def calc_collage_grid(total):
  grid_size = math.sqrt(total)
  if grid_size.is_integer():
    rows, cols = (int(grid_size), int(grid_size))
  else:
    rows, cols = (math.floor(grid_size), math.ceil(grid_size))
    if (rows * cols) > total:
      cols -= 1
  return (rows, cols)

def make_collage(directory, wallpaper):
  product = "wallpaper" if wallpaper else "collage"

  pics = []
  if directory:
    pics = glob.glob(directory + '/*' + globals.image_ext)
  pics = [Image.open(i) for i in pics]

  if globals.verbose:
    print("Total unique images found in directory: %d" % (len(pics)))

  if wallpaper:
    rows,cols = calc_wallpaper_grid(len(pics))
  else:
    rows,cols = calc_collage_grid(len(pics))

  print("Creating %s using %d images from %s" %
        (product, rows*cols, directory))

  if globals.verbose:
    print("Rows: %d Cols: %d" % (rows, cols))

  x_border = 0
  y_border = 0

  if wallpaper:
    x_border,y_border = calc_wallpaper_border(rows, cols)

  # create new blank image of size cols * rows
  x_image_size = globals.image_size
  y_image_size = globals.image_size
  x_row_size = (x_image_size * cols) + (x_border * 2)
  y_row_size = (y_image_size * rows) + (y_border * 2)

  if globals.verbose and wallpaper:
    final_ratio = x_row_size / y_row_size
    print("Result wallpaper ratio: %f" % final_ratio)

  collage = Image.new('RGB', (x_row_size, y_row_size))
  y_offset = y_border

  count = 0
  for row in range (0, rows):
    # create new image the size of one row
    new_row = Image.new('RGB', (x_row_size, y_image_size))
    x_offset = x_border

    # fill row image with images
    for col in range (0, cols):
      new_row.paste(pics[count], (x_offset,0))
      count += 1
      x_offset += x_image_size

    # paste row into finished product
    collage.paste(new_row, (0,y_offset))
    y_offset += y_image_size

  if wallpaper:
    # Resize image to closest wallpaper resolution
    collage = collage.resize(get_closest_resolution(globals.wallpaper_ratio,
                                                    x_row_size,
                                                    y_row_size))
    filename = (directory + "_wallpaper" + globals.image_ext)
  else:
    filename = (directory + globals.image_ext)

  collage.save(filename)
  print("%s saved as: %s" % (product, filename))


def test():
  parse = argparse.ArgumentParser(description="Create collage out of similar images")
  parse.add_argument("directory", nargs="?")
  parse.add_argument("-w", "--wallpaper", action="count", default=0, help="Create a wallpaper out of images gathered from Spotify url results")
  parse.add_argument("-v", "--verbose", action="count", default=0, help="See the program working instead of just believing that it is working")

  args = parse.parse_args()
  if args.directory is None:
    print("Directory arg is required!")
    exit(1)

  globals.verbose = args.verbose
  make_collage(args.directory, args.wallpaper)

if __name__ == '__main__':
  test()
