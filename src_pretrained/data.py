from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
from PIL import Image
from io import open
import numpy as np
from util import *

class Data(object):
  def __init__(self, files_list, batch_size):
    self.files_list = files_list
    self.batch_size = batch_size
    self.data = self.prepare_data()
    self.one_epoch_completed = False

    self.batch_start_idx = 0

  def prepare_data(self):
    train_data = []
    with open(self.files_list) as f:
      for line in f.readlines():
        path = line.strip()
        videoid, frameid = Data.get_videoid_frameid(path)
        train_data.append((path, videoid, frameid))
    # shuffle data
    train_data = np.random.permutation(train_data)
    print u'Training on %d image files...' % len(train_data)
    return train_data
  
  def get_next_batch(self):
    curr_batch = self.data[self.batch_start_idx:
                  self.batch_start_idx+self.batch_size]     #works even for last batch
    self.batch_start_idx += self.batch_size
    if (self.batch_start_idx >= len(self.data)):
      self.batch_start_idx = 0
      self.one_epoch_completed = True
    # load images and preprocess
    batch = []
    batch_annot = []
    for image_info in curr_batch:
      img = Image.open(image_info[0])
      img = img.resize((IMG_DIM['height'], IMG_DIM['width']))
      img_arr = np.asarray(img)
      img_arr = img_arr / 255.0                             # normalize to [0,1]
      batch.append(img_arr)
      batch_annot.append((image_info[1], image_info[2]))

    return batch, batch_annot, self.one_epoch_completed

  # gets image filename formatted as "path/to/dir/vid<vidid>_f<frameid>.jpg"
  @staticmethod
  def get_videoid_frameid(path):
    try:
      path = path[:-4]                                      # remove extension
      filename = path[path.rfind(u'/')+1:]                  # remove path to directory
      videoid, frameid = filename.split(u'_')               # split videoid and frameid
      videoid = eval(videoid[3:])                           # extract videoid
      frameid = eval(frameid[1:])                           # extract frameid
      return videoid, frameid
    except:
      sys.exit(u'Invalid file name format!')

    