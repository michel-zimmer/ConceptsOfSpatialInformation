#!/usr/bin/env python
 
# UNIT TESTS
# https://docs.python.org/2/library/unittest.html 
#

import unittest
from utils import _init_log
import numpy as np

from coreconcepts import ALocate, ExLoc, AFields, Entity, ArrFields 

log = _init_log("tests")

class CoreConceptsTest(unittest.TestCase):
    """ Unit tests for module CoreConceptsPy """
    
    def testExample(self):
        self.assertEqual(1+3,4)
        
    def testAnotherExample(self):
        pass
        #print "This is a unit test that fails"
        #self.assertEqual(1+3,5)
        
    def testLocate(self):
        
        figureA = Entity()
        figureB = Entity()
        groundA = Entity()
        groundB = Entity()
        
        self.assertTrue( ExLoc.isAt( figureA, groundA ) )
        self.assertFalse( ExLoc.isPart( figureA, groundA ) )
    
    def testFields(self):
        
        # basic python list of tuples
        basicField = [((0,0),"ul"),((0,1),"ur"),((1,0),"ll"),((1,1),"lr")]
        print basicField
        
        # arrays based on Numpy
        numpyFieldChar = np.array([ ['ul', 'ur'], ['ll', 'lr'] ])
        print "numpyFieldChar\n",numpyFieldChar
        
        # array of floating points
        numpyFieldFloat = np.array([ [.5, .1], [.45, .2] ])
        print "numpyFieldFloat\n",numpyFieldFloat
        
        print "value for 0,0 =", ArrFields.getValue( numpyFieldFloat, [0, 0] )
        print "value for 1,1 =", ArrFields.getValue( numpyFieldFloat, [1, 1] )
        
        #print ArrField.setValue( numpyArr, [0, 1], "new value" )
        ArrFields.setValue( numpyFieldFloat, [0, 1], .2 )
        print "numpyFieldFloat after change\n",numpyFieldFloat
        #print ArrField.getValue( basicArr, [1, 1] )
    
    def testFieldsMapAlgebra(self):
        print "TODO: test map algebra on fields"
        assert False
        
    def testObjects(self):
        print "TODO: test objects"
        assert False
        
    def testArcShpObjects(self):
        """ Import 2 ArcMap shapefiles and test core concept functions """

        #Get objects from shapefiles
        shapefile1 = "data/objects/Rooftops.shp"
        shapefile2 = "data/objects/ViablePVArea.shp"
        layer_src1 = ogr.Open(shapefile1)
        layer_src2 = ogr.Open(shapefile2)
        lyr1 = layer_src1.GetLayer(0)
        lyr2 = layer_src2.GetLayer(0)
        roofObj = lyr1.GetFeature(0)
        pvObj = lyr2.GetFeature(236)

        #test getBounds on roof object - Poultry Science building
        print "\nTest shapefile objects - getBounds for CalPoly roof"
        roofBounds = ArcShpObjects.getBounds(roofObj)
        roofBounds = (round(roofBounds[0],2),round(roofBounds[1],2),round(roofBounds[2],2),round(roofBounds[3],2))
        print "\nBounding box coordinates, UTM Zone 10N, in form (MinX, MaxX, MinY, MaxY):\n",roofBounds,"\n"
        self.assertEqual(roofBounds, (710915.55, 710983.25, 3910040.96, 3910095.28))
        
        #test hasRelation for PV object within roof object
        rel = ArcShpObjects.hasRelation(pvObj,roofObj,'Within')
        self.assertEqual(rel,True)
        
        #test getProprty for Poultry Science building name
        roofName = ArcShpObjects.getProperty(roofObj, 'name')
        self.assertEqual(roofName,"Poultry Science")

        
if __name__ == '__main__':
    unittest.main()
