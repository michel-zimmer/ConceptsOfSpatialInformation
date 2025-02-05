#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Abstract: Derive slope values from a digital elevation model as an example of the focal function from the core concept 'field.'

@OBSOLETE: THESE EXAMPLES ARE BASED ON ARCPY.
"""

__author__ = "Eric Ahlgren"
__copyright__ = "Copyright 2015"
__credits__ = ["Eric Ahlgren"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "March 2015"
__status__ = "Development"

import sys

sys.path = [ '.', '../..' ] + sys.path
from utils import _init_log
from fields import *

log = _init_log("slopeCalc")

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Set environment settings
env.workspace = os.path.join("..","..","..","data","fields")

# Set local variables
inRaster = "CalPolyDEM.tif"
outMeasurement = "DEGREE"

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute Slope
outSlope = Slope(inRaster, outMeasurement)

# Save the output 
outSlope.save(os.path.join("..","..","..","data","fields","tmp","outSlope.tif"))

