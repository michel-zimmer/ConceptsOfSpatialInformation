# -*- coding: utf-8 -*-

"""
 Abstract: These classes are implementations of the core concept 'field', as defined in coreconcepts.py
           The class is written in an object-oriented style.
"""

__author__ = "Eric Ahlgren"
__copyright__ = "Copyright 2014"
__credits__ = ["Eric Ahlgren", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = ""
__email__ = ""
__date__ = "December 2014"
__status__ = "Development"

import numpy as np
import numpy.ma as ma
import gdal
from gdalconst import *

from utils import _init_log
from coreconcepts import CcField

import ogr
import osr

log = _init_log("fields")

def getGtiffOffset( gtiff, position ):
    """
    Convert GeoTiff coordinates to matrix offset. Used for getValue GeoTiffField method and focal mean function.
    @param position - the input geocoordinates in coordinate system of gtiff
    @return - the i,j pair representing input position in the image matrix
    """
    transform = gtiff.GetGeoTransform()
    #Convert geo-coords to (i,j) image space coordinates
    ulx = transform [0]
    uly = transform [3]
    xQuery = position [0]
    yQuery = position [1]
    pixWidth = transform [1]
    pixHeight = transform [5]
    arrx = int((xQuery - ulx)/pixWidth)
    arry = int((yQuery - uly)/pixHeight)
    return arry, arrx

def FieldGranularity(CcGranularity):
    # TODO:
    def __init__( self, x, y ):
        pass

class GeoTiffField(CcField):
    """
    Subclass of Abstract Fields (core concept 'field') in the GeoTiff format. Based on GDAL.

    Map algebra based on Worboys & Duckham (2004), precise definitions from the text are included with each function.

    Worboys, Michael, and Matt Duckham. GIS : a computing perspective. Boca Raton, Fla: CRC Press, 2004. Print.

    """
    def __init__( self, filepath ):

        """
        @param filepath path to the GeoTiff field
        """
        # assert operation in ['inside','outside']
        self.gField = gdal.Open( filepath, GA_Update ) # open file via gdal
        if self.gField is None:
            print "error: gField is none"


        print 'Driver: ', self.gField.GetDriver().ShortName,'/', \
              self.gField.GetDriver().LongName
        print 'Size is ',self.gField.RasterXSize,'x',self.gField.RasterYSize, \
              'x',self.gField.RasterCount
        print 'Projection is ',self.gField.GetProjection()

        self.cols = self.gField.RasterXSize
        self.rows = self.gField.RasterYSize
        self.domain_geoms = () # tuple [geometry, 'inside'|'outside']

    def value_at( self, position ):
        """
        Returns the value of a raster pixel at an input position.

        @param position the coordinate pair in self's coordinate system
        @return the raw value of the pixel at input position in self or None if it is outside of the domain
        """
        if self._is_in_domain(position):
            offset = getGtiffOffset( self.gField, position )
            array = self.gField.ReadAsArray( offset[1],offset[0], 1,1 ) #Convert image to NumPy array
            return array
        else: return None


    def domain(self):
        # TODO: implement
        raise NotImplementedError("domain")


    def restrict_domain(self, geometry, operation ):
        """
        Restricts the domain to the specified geometry based on inside/outisde operation

        @param geometry, operation
        """
        self.domain_geoms = [geometry.bounds(), operation] # setting to the bounding box of geometry

        print "IN RESTRICT DOMAIN", geometry
        print "GEOMETRY BOUNDS", geometry.bounds() #prints env
        print type(geometry.bounds())
        print type(self.domain_geoms[0])
        print "DOMAIN GEOMS", self.domain_geoms
        print "GEO TRANSFORM", self.gField.GetGeoTransform()
        print "SELF.COLS", self.cols
        print "RASTER X SIZE: ",self.gField.RasterXSize

        (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = self.gField.GetGeoTransform()
        x_calc = upper_left_x + (x_size / 2) # add half the cell size
        y_calc = upper_left_y + (y_size / 2) # to centre the point

        for j in range(self.rows):     # iterate each Y value
            for i in range(self.cols): # iterate each X value
                coords = ( (i+1)*x_size + x_calc, (j+1)*y_size + y_calc ) # assign current cell's calculated coordinates
                if self._is_in_domain(coords): # determine if these new coordinates are within domain_geoms
                    #print "hi"
                    # TODO: set self.domain_geoms; how do we add this to the domain_geoms? do we need a new variable instead?
                    pass


    def _is_in_domain(self, position ):
        """
        Checks if the current cell position is appropriately inside/outside domain_geoms

        @param position
        @return True if position is in the current domain or False otherwise
        """
        geom = self.domain_geoms[0] # retrieve geometry, first part of touple
        inside_outside = self.domain_geoms[1] # TODO: implement so that we can use inside / outside

        if position[0] > float(geom[0]) and position[0] < float(geom[1]): # if position is within X geom
            if position[1] > float(geom[2]) and position[1] < float(geom[3]): # if position is within Y geom
                return True
            else: return False
        else: return False


    def zone( self, position ):
        """
        Return a masked array representing the zone for the input position
        @param position - i,j coordinates from which to derive zone
        @return - NumPy masked array representing the geometry of the zone for pixel at input position
        """
        array = self.gField.ReadAsArray()
        val = array[position[0], position[1]]
        maskArray = ma.masked_not_equal( array, val )  #All values not equal to zone value of input are masked
        return maskArray

    def local( self, fields, localFunc, newGtiffPath ):
        """
        Assign a new value to each pixel in gtiff based on func. Return a new GeoTiff at newGtiffPath.

        "Local operations

        A local operation acts upon one or more spatial fields to produce a new field. The distinguishing feature
        of a local operation is that the value is dependent only on the values of the input field functions at that location.
        Local operations may be unary (transforming a single field), binary (transforming two fields), or n-ary (transforming
        any number of fields).

        1. For each location x, h(x) = f(x) dot g(x)" (Worboys & Duckham 148)

        @param fields - other input fields
        @param localFunc - the local function to be applied to each value in GeoTiff
        @param newGtiffPath - file path for the new GeoTiff
        @return N/A; write new raster to newGtiffPath
        """
        oldArray = self.gField.ReadAsArray()
        newArray = localFunc(oldArray, fields)
        # TODO: update to handle input fields
        driver = self.gField.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        newArray = np.around(newArray.astype(np.double), 3)
        outBand.WriteArray(newArray)
        outBand.FlushCache()

    def average_fields(oldArray, fields):
        pass


    def focal( self, fields, kernFunc, newGtiffPath ):
        """
        Assign a new value to each pixel in self based on focal map algebra. Return a new GeoTiff at filepath newGtiffPath.

        "Focal operations

        For a focal operation the attribute value derived at a location x may depend not only on the attributes of the input
        spatial field functions at x, but also on the attributes of these functions in the neighborhood n(x) of x. Thus, the
        value of the derived field at a location may be influenced by the values of the input field nearby that location.

        For each location x:
        1. Compute n(x) as the set of neighborhood points of x (usually including x itself).
        2. Compute the values of the field function f applied to appropriate points in n(x).
        3. Derive a single value phi(x) of the derived field from the values computed in step 2, possibly taking special account
        of the value of the field at x." (Ibid. 148-9)

        @param newGtiffPath - the filepath of the output GeoTiff
        @param kernFunc - the neighborhood function which returns the kernel array
        @return N/A; write new raster to newGtiffPath
        TODO: Make newGtiffPath optional
        """

        oldArray = self.gField.ReadAsArray()
        newArray = oldArray.copy()
        rows = oldArray.shape[0]
        cols = oldArray.shape[1]
        for i in range (1, rows-1):
            for j in range (1, cols-1):
                newVal = kernFunc(oldArray,(i,j))
                newVal = np.round(newVal, 3)
                newArray.itemset((i,j), newVal)
        driver = self.gField.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        newArray = np.around(newArray.astype(np.double), 3)
        outBand.WriteArray(newArray)
        outBand.FlushCache()

    def zonal( self, fields, zoneFunc, newGtiffPath ):
        """
        Assign a new value to self based on zonal map algebra. Return a new GeoTiff at filepath newGtiffPath.

        "Zonal operations

        A zonal operation aggregates values of a field over each of a set of zones (arising in general from another field function)
        in the spatial framework. A zonal operation zeta derives a new field based on a spatial framework F, a spatial field f, and
        set of k zones {Z1,…,Zk} that partitions F.

        For each location x:
        1. Find the zone Zi in which x is contained.
        2. Compute the values of the field function f applied to each point in Zi.
        3. Derive a single value zeta(x) of the new field from the values computed in step 2." (Ibid. 149-50)

        @param newGtiffPath - the filepath of the output GeoTiff
        @param zoneFunc - the zonal function, which returns a new value for each pixel based on zonal operation
        @return N/A; write new raster to newGtiffPath
        """

        oldArray = self.gField.ReadAsArray()
        newArray = oldArray.copy()
        rows = oldArray.shape[0]
        cols = oldArray.shape[1]
        for i in range (0, rows):
            for j in range (0, cols):
                newVal = zoneFunc(oldArray, (i,j))
                newArray.itemset((i,j), newVal)
        driver = self.gField.GetDriver()
        newRaster = driver.CreateCopy(newGtiffPath, self.gField)
        outBand = newRaster.GetRasterBand(1)
        newArray = np.around(newArray.astype(np.double), 3)
        outBand.WriteArray(newArray)
        outBand.FlushCache()

    def coarsen(self, granularity, func ):
        """
        Constructs new field with lower granularity.

        Default strategy: mean
        @param granularity a FieldGranularity
        @param aggregation strategy func
        @return a new coarser field
        """
        pass
        # TODO: implement with 'aggregate' in GDAL
        # default strategy: mean
        # http://gis.stackexchange.com/questions/110769/gdal-python-aggregate-raster-into-lower-resolution




# TO GET RID OF
def GetExtent(gt,cols,rows):
    ''' Return list of corner coordinates from a geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: number of columns in the dataset
        @type rows:   C{int}
        @param rows: number of rows in the dataset
        @rtype:    C{[float,...,float]}
        @return:   coordinates of each corner
    '''
    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])
            print x,y
        yarr.reverse()
    return ext

def ReprojectCoords(coords,src_srs,tgt_srs):
    ''' Reproject a list of x,y coordinates.

        @type geom:     C{tuple/list}
        @param geom:    List of [[x,y],...[x,y]] coordinates
        @type src_srs:  C{osr.SpatialReference}
        @param src_srs: OSR SpatialReference object
        @type tgt_srs:  C{osr.SpatialReference}
        @param tgt_srs: OSR SpatialReference object
        @rtype:         C{tuple/list}
        @return:        List of transformed [[x,y],...[x,y]] coordinates
    '''
    trans_coords=[]
    transform = osr.CoordinateTransformation( src_srs, tgt_srs)
    for x,y in coords:
        x,y,z = transform.TransformPoint(x,y)
        trans_coords.append([x,y])
    return trans_coords




    ## WITHIN RESTRICT DOMAIN


        # a = self.gField.ReadAsArray().astype(np.float)
        # (y_index, x_index) = np.nonzero(a > threshold)
        # (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = self.gField.GetGeoTransform()
        # x_coords = x_index * x_size + upper_left_x + (x_size / 2) #add half the cell size
        # y_coords = y_index * y_size + upper_left_y + (y_size / 2) #to centre the point


        # for row in self.gField.ReadAsArray():
        #     for col in row:
        #         x_pos = col * x_size + upper_left_x + (x_size / 2) #add half the cell size
        #         y_pos = row[1] * y_size + upper_left_y + (y_size / 2) #to centre the point
        #         coords = (x_pos,y_pos)
        #         # print coords
        #         self.value_at(coords)
        #         #print "in for loop"
        #         #print coords

        # ext=GetExtent(self.geoTransform, self.cols, self.rows)
        #
        # src_srs=osr.SpatialReference()
        # src_srs.ImportFromWkt(self.gField.GetProjection())
        # tgt_srs = src_srs.CloneGeogCS()
        #
        # geo_ext=ReprojectCoords(ext,src_srs,tgt_srs)

        # print "GEO EXTENT", geo_ext

        # cols = self.gField.RasterXSize
        # rows = self.gField.RasterYSize
        # allBands = self.gField.RasterCount
        # print allBands
        #
        # band = self.gField.ReadAsArray(0,0,cols,rows)
        # band2 = self.gField.ReadAsArray().astype(np.float)
        #
        # thing = self.gField.GetGeoTransform()
        # print "THING", thing

   ## WITHIN IS_IN_DOMAIN
        # if position[0] in range(float(geom[0]), float(geom[1])):
        #     if position[1] in range(float(geom[2]), float(geom[3])):
        #         print "it is"
        #         pass
        #         #return True
        #     pass
        # else:
        #     pass
