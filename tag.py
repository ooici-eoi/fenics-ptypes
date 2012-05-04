#!/usr/bin/env python

"""
@package
@file fenics-ptypes/tag.py
@author Christopher Mueller
@author David Stuebe
@brief Tag object similar to MOAB for fenics mesh and mesh functions
"""

from dolfin import MeshFunction, Mesh, MeshEntity, MeshEditor, Vertex, Cell, vertices, cells
import numpy

def ion_ehandle(entity):
    """
    Handle is an internal concern of tags - it should never be exposed outside the tag.
    """
    #@todo handle attribute errors...
    return entity.dim(), entity.index()


class IonTag(object):

    def __init__(self, name, size, type, mesh):

        #@todo - add exception handling
        assert(isinstance(name, str))
        assert(isinstance(size, int))
        assert(size > 0)
        assert(isinstance(mesh, Mesh))

        self._name = name
        self._size = size
        self._type = type
        self._mesh = mesh

        #@todo - can we pass/use a memory mapped object?
        self._value_func = lambda x: numpy.fromiter(x, dtype=self._type, count=self._size)

        self._entity_values={}

    def __getitem__(self, entity):
        return self._entity_values[ion_ehandle(entity)]


    def __setitem__(self, entity, values):
        assert entity.mesh().id() is self._mesh.id(), 'Do not put entities from different meshes in the same tag!'
        #@todo - check the length what should we do if it doesn't match?
        self._entity_values[ion_ehandle(entity)] = self._value_func(values)

    def __iter__(self): # real signature unknown; restored from __doc__
        """ x.__iter__() <==> iter(x) """
        pass

    def __len__(self): # real signature unknown; restored from __doc__
        """ x.__len__() <==> len(x) """
        return len(self._entity_values)

    def __delitem__(self, y): # real signature unknown; restored from __doc__
        """ x.__delitem__(y) <==> del x[y] """
        del self._entity_values[y]

    def __contains__(self, k): # real signature unknown; restored from __doc__
        """ D.__contains__(k) -> True if D has a key k, else False """

        return self._entity_values.has_key(k)

    def iteritems(self): # real signature unknown; restored from __doc__
        """ D.iteritems() -> an iterator over the (key, value) items of D """
        for k, v in self._entity_values.iteritems():
            #@todo - how do we get the entity back rather than our handle???
            yield MeshEntity(self._mesh, *k), v


    def iterkeys(self): # real signature unknown; restored from __doc__
        """ D.iterkeys() -> an iterator over the keys of D """
        for k in self._entity_values.iterkeys():
            #@todo - how do we get the entity back rather than our handle???
            yield MeshEntity(self._mesh, *k)

    def itervalues(self): # real signature unknown; restored from __doc__
        """ D.itervalues() -> an iterator over the values of D """
        for v in self._entity_values.itervalues():
            #@todo - how do we get the entity back rather than our handle???
            yield v


mesh = Mesh()
editor = MeshEditor()
editor.open(mesh, 2, 2) # topo_dim = 2, geom dim = 2

editor.init_vertices(6)
editor.init_cells(2)

vertex_0 = Vertex(mesh, 0)
vertex_1 = Vertex(mesh, 1)
vertex_2 = Vertex(mesh, 2)
vertex_3 = Vertex(mesh, 3)

vertex_4 = Vertex(mesh, 4)
vertex_5 = Vertex(mesh, 5)

editor.add_cell(0,1,2,3)
editor.add_cell(1,0,2,3)

editor.close()


t = IonTag('foo',3,'int', mesh)

for v in vertices(mesh):
    t[v] = [1,2,3]

for c in cells(mesh):
    t[c] = [4,5,6,7]



v = MeshEntity(mesh,0,1)

print t[v]

