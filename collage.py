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


def make_collage(directory):

  pics = []
  if directory:
    pics = glob.glob(directory + '/*.jpeg')
  pics = [Image.open(i) for i in pics]

  if globals.verbose:
    print("Total unique pictures: " + str(len(pics)))

  rows,cols = calc_size(len(pics))

  if globals.verbose:
    print("Rows: " + str(rows) + "\tCols: " + str(cols))

  # create new blank image of size cols * rows
  x_image_size = globals.image_size + globals.image_x_border
  y_image_size = globals.image_size + globals.image_y_border
  x_row_size = (x_image_size * cols) + globals.image_x_border
  y_row_size = (y_image_size * rows) + globals.image_y_border

  collage = Image.new('RGB', (x_row_size, y_row_size))
  y_offset = globals.image_y_border
  count = 0;
  
  for row in range (0, rows):
    # create new image the size of one row
    new_row = Image.new('RGB', (x_image_size * cols, y_image_size))
    x_offset = globals.image_x_border

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

