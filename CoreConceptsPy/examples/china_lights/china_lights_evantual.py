import sys
import os
import unittest
import numpy as np
import random

sys.path = [ '.', '..', '../..', '../../..' ] + sys.path

from CoreConceptsPy.coreconcepts import *

def calculate_luminosity():

    # create fields & objects from file path
    china_boundary = CcObject('data/china.shp')
    china_lights_1 = CcField('data/lights_1994a.tif').restrict_domain(china_boundary, 'inside')
    china_lights_2 = CcField('data/lights_1994b.tif').restrict_domain(china_boundary, 'inside')
    gas_flares = CcObject('data/china_flares.shp')

    # average fields
    luminosity = china_lights_1.local(china_lights_2, 'average')

    # remove gas flares
    luminosity.restrict_domain(gas_flares, 'outside')

    # create roads buffer
    roads = CcObject('data/china_roads.shp')
    roads_buffered = buffer(roads, 0.5)

    # restrict domain of luminosity to road buffer
    luminosity_around_roads = luminosity.restrict_domain(luminosity, roads_buffered, 'inside')

    # aggregate previous information
    results = luminosity_around_roads.coarsen(0.1, 0.1)

def main():
    calculate_luminosity()

if __name__ == '__main__':
    main()


    ##### --> THOMAS' IDEAL FINAL IMPLEMENTATION

    ## china          = CcObject('data/china.shp')
    ## gas_flares     = CcObject('data/china_flares.shp')
    ## china_lights_1 = CcField('data/lights_1994a.tif').inside(china)
    ## china_lights_2 = CcField('data/lights_1994b.tif').inside(china)

    ## fields = [china_lights_1, china_lights_2]

    ## luminosity = average(fields, local)
    ## luminosity.outside(gas_flares) #same as outside

    ## roads_buffered = CcObject('data/china_roads.shp').buffer(0.5)
    ## luminosity.inside(roads_buffered)
    ## luminosity.aggregate(5)