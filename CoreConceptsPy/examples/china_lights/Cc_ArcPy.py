# -*- coding: utf-8 -*-
import os
import arcpy
from arcpy import env
from arcpy.sa import *
# Set working directory
env.workspace = "C:\Users\lafia\Desktop\chinalights_data"
workspace = env.workspace
arcpy.env.overwriteOutput = True

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")


class CcField(object):
    """
    Class defining abstract field.
    Based on Field.hs
    """
    def __init__(self, filepath, domain):
        self.filepath = filepath
        self.domain = domain
        """ Define appropriate parameters for construction of the concrete object """
        # TODO: restrict value pairs to geoObject
        #, fieldFunction, geoObject, geoEvent
        #self.geoObject = geoObject
        #self.geoEvent = geoEvent
        pass

    def makeField(filepath):
        desc = arcpy.Describe(filepath)
        domain = desc.extent
        #return eval(type + "()")
        if filepath.endswith(".tif"):
            #geoObject = arcpy.env(test_filepath)
            return GeoTiffField(filepath, domain)
        elif filepath.endswith(".mp3"): return TestField()
        assert 0, "Bad shape creation: " + filepath
    makeField = staticmethod(makeField)

    def value_at( self, position ):
        """
        @return the value of field at position, or None if it is outside of the domain.
        """
        # TODO: check if position falls within value
        raise NotImplementedError("valueAt")

    def domain( self ):
        """
        @return current domain of the field
        """
        raise NotImplementedError("domain")

    def restrict_domain(self, object, operation ):
        pass


    def local( self, fields, fun ):
        """
        Uses raster calculator from ArcPy
        TODO: make a general funtion for more than two fields
        """
        if fun == 'average':
            test = arcpy
            output = (arcpy.Float(self.filepath)+arcpy.Float(fields.filepath))/2

        elif fun == 'maximum':
            #TODO complete list of local operations
            output = (arcpy.Float(self.filepath)+arcpy.Float(fields.filepath))/2

        else:
            print 'the input function is not defined'

        return output
        #average_luminosity.save("FXX1994")

class CcObject(object):
    """
    Abstract class for core concept 'object'
    Based on Object.hs
    """
    def __init__( self, filepath, objIndex, domain ):
        self.filepath = filepath
        self.sObj = objIndex
        self.domain = domain

    def makeObject(filepath):
        desc = arcpy.Describe(filepath)
        domain = desc.extent
        #return eval(type + "()")
        if filepath.endswith(".shp"):
            return ArcShpObject(filepath, 1, domain) #TODO: alter objIndex
        elif filepath.endswith(".mp3"):
            return TestField()
        assert 0, "Bad shape creation: " + filepath
    makeObject = staticmethod(makeObject)

    def bounds( self ):
        raise NotImplementedError("bounds")

    def relation( self, obj, relType ):
        """ @return Boolean True if self and obj are in a relationship of type relType
                    False otherwise
        """
        raise NotImplementedError("relation")

    def property( self, prop ):
        """
        @param prop the property name
        @return value of property in obj
        """
        raise NotImplementedError("property")

    def identity( self, obj ):
        """
        @param an object
        @return Boolean True if self and obj are identical
        """
        raise NotImplementedError("identity")

class CcGranularity:
    def __init__(self):
        pass
        # TODO: cell_size_x, cell_size_y

###############################################################

class GeoTiffField(CcField):
    def __init__(self, filepath, domain):
        #, fieldFunction, geoObject, geoEvent
        super(GeoTiffField, self).__init__(filepath, domain)
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.domain = domain

        #self.geoObject = geoObject
        #env.workspace = "C:\Users\lafia\Desktop\chinalights_data"

    def value_at(self, value_at): print(value_at)

    def restrict_domain(self, object, operation ):
        """
        @param domain a domain to be subtracted to the current domain
        """
        if operation == 'inside':

            # arcpy.env.mask = object.filepath
            # print("test:",arcpy.env.mask)


            # # print("object.domain: ", object.domain)
            # # env.workspace.extent = object.domain
            # # arcpy.RasterToPolygon_conversion(self, "selfPolygon.shp")
            # arcpy.env.snapRaster = self.filepath #TODO: will resolve output shift
            # # mask(self, object)


            # print("self.filename: ", self.filename, "self.domain: ", self.domain, " before")
            # print("object.domain", object.domain)
            output = arcpy.sa.ExtractByMask(self.filename, object.filename)
            # print("output: ", type(output))
            (nfilepath, nfilename) = os.path.split(self.filepath)

            outputLocation = nfilepath + "\_masked_" + nfilename
            output.save(outputLocation)

            desc = arcpy.Describe(outputLocation)
            self.domain = desc.extent
            self.filepath = outputLocation
            self.filename = os.path.basename(outputLocation)

            print("self.filename: ", self.filename, "self.domain: ", self.domain, " after")

            # print("restricted success")
            # print(output)
            # print(type(output))
            # print(arcpy.Describe(outputLocation))
            # print(outputLocation)
            # myMaskedField = CcField.makeField(outputLocation)
            # print "print myMaskedField: ", myMaskedField
            # print("print myMaskedField type: ", type(myMaskedField))

        elif operation == 'ouside':
            # temp = arcpy.RasterToPolygon_conversion(self, "selfPolygon.shp")
            # #erase(self, object)
            # output = arcpy.Erase_analysis(temp, object, "output_class.shp")
            # return output
            pass

    def local( self, fields, fun ):
        """
        Uses raster calculator from ArcPy
        TODO: make a general funtion for more than two fields
        """
        if fun == 'average':
            print("averaging")
            output = (Float(self.filepath)+ Float(fields.filepath))/2

            #(nfilepath, nfilename) = os.path.split(self.filepath)

            (nfilepath, nfilename) = os.path.split(self.filepath)

            outputLocation = nfilepath + "\_averaged" + nfilename
            output.save(outputLocation)

            desc = arcpy.Describe(outputLocation)
            self.domain = desc.extent
            self.filepath = outputLocation
            self.filename = os.path.basename(outputLocation)

            print("self.filename: ", self.filename, "self.domain: ", self.domain, " after")

        elif fun == 'maximum':
            #TODO complete list of local operations
            output = (Float(self.filepath)+Float(fields.filepath))/2

        else:
            print 'the input function is not defined'

        return output

class TestField(CcField):
    pass

class ArcShpObject(CcObject):
    def __init__( self, filepath, objIndex, domain ):
        super(ArcShpObject, self).__init__(filepath, objIndex, domain)
        self.filepath = filepath
        self.sObj = objIndex
        self.domain = domain
        self.filename = os.path.basename(filepath)

    def buffer ( self, object, distance ):
        output = arcpy.Buffer_analysis(self.filename, object.filenameFull)
