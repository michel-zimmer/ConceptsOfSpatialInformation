# -*- coding: utf-8 -*-

"""
 Abtract: These classes are the specifications of the core concepts, adapted from the Haskell.
          The classes are written in an object-oriented style.
"""

__author__ = "Werner Kuhn and Andrea Ballatore"
__copyright__ = "Copyright 2014"
__credits__ = ["Werner Kuhn", "Andrea Ballatore"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Andrea Ballatore"
__email__ = ""
__date__ = "August 2014"
__status__ = "Development"

from utils import _init_log
import abc

log = _init_log("coreconcepts")

class CcLocation(object):
    """
    Class defining abstract location relations
    Note: Unused for the moment.
    """

    def isAt( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isAt")

    def isIn( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isIn")

    def isPart( figure, ground ):
        """
        @return Bool
        """
        raise NotImplementedError("isPart")

class CcField(object):
    """
    Class defining abstract field.
    Based on Field.hs
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, *filepath):
        """ Define appropriate parameters for construction of the concrete object """
        _determine_type(self, filepath)

        pass

    @abc.abstractmethod
    def value_at( self, position ):
        """ 
        @return the value of field at position, or None if it is outside of the domain.
        """
        raise NotImplementedError("valueAt")

    def domain( self ):
        """
        @return current domain of the field
        """
        raise NotImplementedError("domain")
    
    def restrict_domain(self, geometry, operation ):
        """ 
        @param domain a domain to be subtracted to the current domain  
        """
        raise NotImplementedError("restrict_domain")

    def _is_in_domain(self, position ):
            """
            @param position
            @return True if position is in the current domain or False otherwise
            """
            # TODO: implement using self.domain_geoms

    def rect_neigh( self, position, width, height ):
        """
        Map algebra: rectangular neighborhood function
        @return Geometry (a field mask)
        """
        raise NotImplementedError("rectNeigh")

    def zone( self, position ):
        """
        Map algebra: zone function
        @return Geometry (a field mask)
        """
        raise NotImplementedError("zone")

    def local( self, fields, fun ):
        """
        Map algebra's local operations, with a function to compute the new values
        @param fields other fields
        @return new CcField field
        """
        raise NotImplementedError("local")

    def focal( self, fields, fun ):
        """
        Map algebra's focal operations, with a kernel function to compute the new values based on the neighborhood of the position
        @return new CcField field
        """
        raise NotImplementedError("focal")

    def zonal( self, fields, fun ):
        """
        Map algebra's zonal operations, with a function to compute the new values based on zones containing the positions.
        @return new CcField field
        """
        raise NotImplementedError("zonal")

class CcObject(object):
    """
    Class defining abstract object.
    Based on Object.hs
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, filepath):
        """ Define appropriate parameters for construction of the concrete object """
        pass

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

class CcObjectSet(object):
    """
    Set class for object sets
    """
    def __init__(self):
        self.obj_set = set()
    
    def add(self, obj ):
        assert obj is not None
        self.obj_set.add(obj)
    
    def remove(self, obj):
        self.obj_set.remove(obj)

class CcNetwork(object):
    """
    Abstract class for core concept 'network'
    Based on Network.hs
    """

    def __init__(self):
        pass

    def nodes( self, data = False ):
        """ @return a copy of the graph nodes in a list """
        raise NotImplementedError("nodes")

    def edges( self, data = False ):
        """ @return list of edges """
        raise NotImplementedError("edges")

    def addNode( self, n, **attr ):
        """ Add node n with the attributes attr """
        raise NotImplementedError("addNode")

    def addEdge( self, u, v, **attr ):
        """ Add an edge with the attributes attr between u and v """
        raise NotImplementedError("addEdge")

    def connected( self, u, v ):
        """ @return whether node v can be reached from node u """
        raise NotImplementedError("connected")

    def shortestPath( self, source, target, weight = None ):
        """ @return shortest path in the graph """
        raise NotImplementedError("shortestPath")

    def degree( self, n ):
        """ @return number of the nodes connected to the node n """
        raise NotImplementedError("degree")

    def distance( self, source, target ):
        """ @return the length of the shortest path from the source to the target """
        raise NotImplementedError("distance")

    def breadthFirst( self, node, distance ):
        """ @return all nodes within the distance from node in this network """
        raise NotImplementedError("breadthFirst")

class CcEvent(object):
    """
    Abstract class for core concept 'event'.
    Based on Event.hs
    """

    def __init__(self):
        pass

    def within( self ):
        """
        @return a Period
        """
        raise NotImplementedError("within")

    def when( self ):
        """
        @return a Period
        """
        raise NotImplementedError("when")

    def during( self, event ):
        """
        @param event an event
        @return boolean
        """
        raise NotImplementedError("during")

    def before( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("before")

    def after( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("after")

    def overlap( self, event ):
        """
        @param event an event
        @return Boolean
        """
        raise NotImplementedError("overlap")

class CcGranularity:
    def __init__(self):
        pass
        # TODO: cell_size_x, cell_size_y