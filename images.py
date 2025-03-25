################################################################################
# Author: Orion Crocker
# Filename: images.py
# Date: 02/06/20
# 
# Get Spotify Album Art
# Retrieves album art from Spotify's spotify
################################################################################

import api
import os
import requests
from zipfile import ZipFile
import globals


def zip_images(directory):
  zip_this = ZipFile(directory + '.zip', 'w')
  os.chdir(directory)
  for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
      zip_this.write(file)
  zip_this.close()


def get_images(url):
  urls,name = api.get_image_list_and_name(url)

  if len(urls) == 0:
    print("No results found, check URL and try again.")
    exit(1)
  else:
    print("%d unique album art URLs found!" % (len(urls)))

  if globals.user_dir:
    directory = globals.user_dir + '/' + api.clean_string(name)
  else:
    directory = 'results/' + api.clean_string(name)

  if not os.path.exists(directory):
      os.makedirs(directory)

  pics = []

  for name, url in urls:
    path = directory + "/" + name + ".jpeg"
    if os.path.exists(path):
      continue

    pic = requests.get(url, allow_redirects=True)

    if globals.verbose:
      print(path)

    open(path, 'wb').write(pic.content)
    pics.append(pic)

  print("%d saved to %s" % (len(pics), directory))

  if globals.zip_results:
    zip_images(directory)

  return directory
