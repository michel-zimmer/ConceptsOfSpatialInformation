import sys
import os
import unittest
import numpy as np
import random

sys.path = [ '.', '..', '../..', '../../..' ] + sys.path

######### THIS IS ALL PSEUDO-CODE ############
from CoreConceptsPy.fields import GeoTiffField
from CoreConceptsPy.objects import ArcShpObject, ArcShpObjectSet

# setting up our initial data [load, average, restrict domain, remove]
def part_1():
    # create file path arguments
    file_path_1 = 'data/lights_1994a.tif'
    file_path_2 = 'data/lights_1994b.tif'
    file_path_3 = 'data/china_flares.shp'
    file_path_4 = 'data/china.shp'

    # create objects from file path

    china = ArcShpObject(file_path_4)
    print china

    china_flares = ArcShpObjectSet(file_path_3)
    print china_flares

    # create fields from file path
    china_field_a = GeoTiffField(file_path_1).restrict_domain(china, 'inside')
    print china_field_a

    china_field_b = GeoTiffField(file_path_2)
    print china_field_b

#
#     # perform local averaging operation
#     luminosity = china_field_a.local(china_field_b, average)
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
