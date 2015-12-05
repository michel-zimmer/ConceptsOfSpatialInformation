import sys
import os
import unittest
import numpy as np
import random

sys.path = [ '.', '..', '../..', '../../..' ] + sys.path

from CoreConceptsPy.coreconcepts import *

def calculate_luminosity():
    # create file path arguments
    file_path_1 = 'data/lights_1994a.tif'
    file_path_2 = 'data/lights_1994b.tif'
    file_path_3 = 'data/china_flares.shp'
    file_path_4 = 'data/china.shp'

    # create fields & objects from file path
    china_boundary = CcObject(file_path_4)
    china_field_a = CcField(file_path_1).restrict_domain(china_boundary)
    china_field_b = CcField(file_path_2).restrict_domain(china_boundary)
    china_flares = CcObject(file_path_3)

    luminosity = china_field_a.local(china_field_b, average)
    # TODO: fields = [file_path_1, file_path_2, file_path_3, file_path_4]
    # TODO: new_field = average(fields, local) # ? another argument that allows users to 'use lenses' to look at the inputs the way the user wants (determine type)
    # TODO: what are you doing? you are taking an average (doing something), and then defining how to do it (local)

    # remove gas flares
    luminosity = set_domain(luminosity, china_flares, outside)
    # TODO: luminosity.remove(gas_flares)

    # create file path arguments
    file_path_5 = 'data/china_roads.shp' # need to get the data for this

    # create objects from file path
    roads = CcObject(file_path_5)
    roads_buffered = buffer(roads, 0.5)

    # restrict domain of luminosity to road observation
    luminosity_around_roads = set_domain(luminosity, roads_buffered, inside)
    # TODO: luminosity.set_domain(roads_buffered)

    # aggregate previous information
    final = luminosity_around_roads.coarsen(0.1, 0.1)
    # TODO: luminosity.aggregate(5) #upscale by 5x

def main():
    calculate_luminosity()

if __name__ == '__main__':
    main()
