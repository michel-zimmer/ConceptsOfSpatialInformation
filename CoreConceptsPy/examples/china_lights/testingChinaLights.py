# Import arcpy module
import arcpy
from arcpy import env
from arcpy.sa import *

# arcpy.CheckOutExtension("spatial")

from coreConcepts.coreconcepts import *

# Set working directory
# env.workspace = "C:\Users\lafia\Desktop\chinalights_data"

# load data
china_boundary = CcObject.makeObject("C:\Users\lafia\Desktop\chinalights_data\China.shp")
china_lights_1 = CcField.makeField("C:\Users\lafia\Desktop\chinalights_data\F101994.tif")
china_lights_1.restrict_domain(china_boundary, 'inside')
china_lights_2 = CcField.makeField("C:\Users\lafia\Desktop\chinalights_data\F121994.tif")
china_lights_2.restrict_domain(china_boundary, 'inside')

# # local - average method
average_luminosity = china_lights_1.local(china_lights_2, 'average')
print("avg_lum filepath: ", average_luminosity.filepath, "avg_lum type: ", type(average_luminosity)) # TODO: determine typing differences

## remove gas flares - erase method

## buffer roads - buffer method

## coarsen granularity - resample method
