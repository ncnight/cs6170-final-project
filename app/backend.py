###
# Utilities and helpers for the application visualization
###
"""
Imports
"""
import numpy as np

"""
Constants
"""
DATA_DIR  = "../data/"
DGM_DIR   = DATA_DIR + "dgms/"
IMG_DIR   = DATA_DIR + "imgs/"
DISTS_DIR = DATA_DIR + "distances/"
HERA_LOC  = "../hera/" #TODO

"""
ad hoc class for neuron representation
"""
class neuron:
    def __init__(self, layer, node_id, img, dgms_color=None, dgms_grey=None, precompute=False):
        self.layer = layer
        self.id    = node_id
        self.img   = img
        self.dgms_color = dgms_color
        self.dgms_grey  = dgms_grey
        #TODO Implement precompute

"""
Helper class that deals with the logic of individual layers
"""
class layer:
    def __init__(model, layer):
        self.__model = model
        self.__layer = layer
