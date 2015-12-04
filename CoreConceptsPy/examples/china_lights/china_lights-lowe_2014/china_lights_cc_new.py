import sys
import os
import unittest
import numpy as np
import random

sys.path = [ '.', '..', '../..', '../../..' ] + sys.path

######### THIS IS ALL PSEUDO-CODE ############
from CoreConceptsPy.coreconcepts import CcField

# setting up our initial data [load, average, restrict domain, remove]
def part_1():
    # create file path arguments
    file_path_1 = 'data/lights_1994a.tif'
    file_path_2 = 'data/lights_1994b.tif'
    file_path_3 = 'data/china_flares.shp'
    file_path_4 = 'data/china.shp'

    # create fields from file path
    china_field_a = CcField(file_path_1)

    china_field_b = CcField(file_path_2)

#     # create objects from file path
#     china_flares = CcObject(file_path_3)
#     china = CcObject(file_path_4)
#
#     # perform local averaging operation
#     luminosity = china_field_a.local(china_field_b, average)
#     # TODO: fields = [file_path_1, file_path_2, file_path_3, file_path_4]
#     # TODO: new_field = average(fields, local) # ? another argument that allows users to 'use lenses' to look at the inputs the way the user wants (determine type)
#     # TODO: what are you doing? you are taking an average (doing something), and then defining how to do it (local)
#
#     # remove gas flares
#     luminosity.remove(china_flares)
#
#     return luminosity
#
# # observe phenomena around roads
# def part_2(luminosity):
#
#     # create file path arguments
#     file_path_5 = 'data/china_roads.shp' # need to get the data for this
#
#     # create objects from file path
#     roads = CcObject(file_path_5)
#     roads_buffered = buffer(roads, 0.5)
#
#     # restrict domain of luminosity to road observation
#     luminosity_around_roads = set_domain(luminosity, roads_buffered, inside)
#
#     return luminosity_around_roads
#
# # coursen granularity (aggregation of lighting information)
# def part_3(luminosity_around_roads):
#
#     # aggregate previous information
#     final = luminosity_around_roads.aggregate(0.1, 0.1)
#     return final


def main():
    print 'Running China Lights case study'
    luminosity = part_1()
    # luminosity_around_roads = part_2(luminosity)
    # final = part_3(luminosity_around_roads)
    print 'OK'

if __name__ == '__main__':
    main()
