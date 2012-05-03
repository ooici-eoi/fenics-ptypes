#!/usr/bin/env python

"""
@package
@file fenics-ptypes/tag.py
@author Christopher Mueller
@author David Stuebe
@brief Tag object similar to MOAB for fenics self.mesh and self.mesh functions
"""



from tag import IonTag, ion_ehandle
import unittest
from create_mesh_no_coords import *
from dolfin import MeshFunction, Mesh, MeshEntity

class TestIonTag(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        self.mesh = Mesh()
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


    def test_init(self):
        # test possible arguments and failure cases...



        pass


    def test_get_set_del(self):
        #Test the getter, setter and delete method

        values = [1,2,3]

        t = IonTag('foo',3,'int', self.mesh)

        v = MeshEntity(self.mesh,0,1)

        # testing setter
        t[v] = values

        # testing getter
        self.assertEqual(t[v], values)

        #@todo: test delete: delete is not yet implemented in tag


    def test_types(self):
        # test with different types:

        # Ints
        t = IonTag('foo',3,'int', self.mesh)


        # Floats
        t = IonTag('foo',3,'float', self.mesh)

        # Complex
        t = IonTag('foo',3,'complex', self.mesh)

        # String
        t = IonTag('foo',3,'string', self.mesh)

        # User defined

        # t = IonTag('foo',3,'user_defined', self.mesh)

        # Object
        t = IonTag('foo',3,'object', self.mesh)


    def test_iter(self):
        # test the iterator and verify that the correct type is passed back


        pass


    def test_properties(self):
        # contains, len etc...
        pass



