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
from PIL import Image
import math
import globals

def calc_size(total):

  grid_size = math.sqrt(total)

  rows = 0
  cols = 0

  if grid_size.is_integer():
    rows, cols = (int(grid_size), int(grid_size))
  else:
    rows, cols = (math.floor(grid_size), math.ceil(grid_size))
    if (rows * cols) > total:
      rows, cols = (math.floor(grid_size), math.floor(grid_size))

  return (rows, cols)

def get_wallpaper_ratio():
  x,y = map(int, globals.wallpaper_ratio.split(':'))
  return x/y

def calc_wallpaper_padding(rows, cols):
  target_ratio = get_wallpaper_ratio()
  current_ratio = cols/rows
  if globals.verbose:
    print("Target ratio: %f" % target_ratio)
    print("Current ratio: %f" % current_ratio)

  x_size = globals.image_size * cols
  x_needed = ((x_size * target_ratio) / current_ratio) - x_size
  x_padding = math.ceil(x_needed / (cols + 1))
  x_total = x_size + (x_padding * (cols + 1))

  # TODO!
  y_padding = 0
  return x_padding,y_padding

def make_collage(directory, wallpaper):
  pics = []
  if directory:
    pics = glob.glob(directory + '/*.jpeg')
  pics = [Image.open(i) for i in pics]

  if globals.verbose:
    print("Total unique pictures: " + str(len(pics)))

  rows,cols = calc_size(len(pics))

  if globals.verbose:
    print("Rows: " + str(rows) + "\tCols: " + str(cols))

  x_padding = 0
  y_padding = 0
  if wallpaper:
    x_padding,y_padding = calc_wallpaper_padding(rows, cols)

  # create new blank image of size cols * rows
  x_image_size = globals.image_size + x_padding
  y_image_size = globals.image_size + y_padding
  x_row_size = (x_image_size * cols) + x_padding
  y_row_size = (y_image_size * rows) + y_padding

  if globals.verbose and wallpaper:
    final_ratio = x_row_size / y_row_size
    print("Result wallpaper ratio: %f" % final_ratio)

  collage = Image.new('RGB', (x_row_size, y_row_size))
  y_offset = y_padding
  count = 0;

  for row in range (0, rows):
    # create new image the size of one row
    new_row = Image.new('RGB', (x_image_size * cols, y_image_size))
    x_offset = x_padding

    # fill row image with images
    for col in range (0, cols):
      new_row.paste(pics[count], (x_offset,0))
      count += 1
      x_offset += x_image_size

    # paste row into finished product
    collage.paste(new_row, (0,y_offset))
    y_offset += y_image_size

  filename = (directory + '.jpeg')

  collage.save(filename)
  print("Collage saved as: " + filename)

