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

def calc_size(total):

  grid_size = math.sqrt(total)

  rows = 0
  cols = 0

  if grid_size.is_integer():
    rows, cols = (int(grid_size), int(grid_size))
  else:
    rows, cols = (math.floor(grid_size), math.ceil(grid_size))

  return (rows, cols)


def make_collage(directory, verbose):

  pics = []
  if directory:
    pics = glob.glob(directory + '/*.jpeg')
  pics = [Image.open(i) for i in pics]

  if verbose:
    print("Total unique pictures: " + str(len(pics)))

  rows,cols = calc_size(len(pics))

  if verbose:
    print("Rows: " + str(rows) + "\tCols: " + str(cols))

  # create new blank image of size cols * rows
  collage = Image.new('RGB', (640 * cols, 640 * rows))
  y_offset = 0
  count = 0;
  
  for row in range (0, rows):
    # create new image the size of one row
    new_row = Image.new('RGB', (640 * cols, 640))
    x_offset = 0

    # fill row image with images
    for col in range (0, cols):
      new_row.paste(pics[count], (x_offset,0))
      count += 1
      x_offset += 640

    # paste row into finished product
    collage.paste(new_row, (0,y_offset))
    y_offset += 640

  filename = (directory + '.jpeg')

  collage.save(filename)
  print("Collage saved as: " + filename)

