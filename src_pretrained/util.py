from __future__ import absolute_import
import numpy as np
import tensorflow as tf
import sys
import functools
from functional import partial, compose

batch_size = 4
LATENT_CODE_SIZE = 2
IMG_DIM = {'width': 240, 'height': 180, 'channels': 3}
BRANCHING_FACTOR = 2
NUM_LEVELS = 3
NUM_INTERNAL_EDGES = BRANCHING_FACTOR * ((BRANCHING_FACTOR ** (NUM_LEVELS-2) - 1) /
                                         (BRANCHING_FACTOR - 1))
NUM_PATHS = BRANCHING_FACTOR ** (NUM_LEVELS - 1)
NUM_NODES = (BRANCHING_FACTOR ** NUM_LEVELS - 1) / (BRANCHING_FACTOR - 1)
NUM_INTERNAL_NODES = NUM_NODES - NUM_PATHS
NUM_EDGES = BRANCHING_FACTOR * ((BRANCHING_FACTOR ** (NUM_LEVELS-1) - 1) / 
                                (BRANCHING_FACTOR - 1))

# ncrp hyperparameters
ALPHA = np.zeros(shape=LATENT_CODE_SIZE)
GAMMA = 10.0
SIGMA_B = 1.0
SIGMA_Z = 200.0
SIGMA_B_sqrinv = 1.0 / (SIGMA_B ** 2)
SIGMA_Z_sqrinv = 1.0 / (SIGMA_Z ** 2)


def composeAll(*args):
    """Util for multiple function composition

    i.e. composed = composeAll([f, g, h])
         composed(x) # == f(g(h(x)))
    """
    # adapted from https://docs.python.org/3.1/howto/functional.html
    return partial(functools.reduce, compose)(*args)

