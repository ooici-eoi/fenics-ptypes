#!/usr/bin/env python

"""
@package
@file fenics-ptypes/tag.py
@author Christopher Mueller
@author David Stuebe
@brief Tag object similar to MOAB for fenics self.mesh and self.mesh functions
"""



from tag import IonTag
import unittest
from dolfin import MeshFunction, Mesh, MeshEntity, MeshEditor, Vertex, vertices

class TestIonTag(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        self.mesh = Mesh()
        editor = MeshEditor()
        editor.open(self.mesh, 2, 2) # topo_dim = 2, geom dim = 2

        editor.init_vertices(6)
        editor.init_cells(2)



        vertex_0 = Vertex(self.mesh, 0)
        vertex_1 = Vertex(self.mesh, 1)
        vertex_2 = Vertex(self.mesh, 2)
        vertex_3 = Vertex(self.mesh, 3)

        vertex_4 = Vertex(self.mesh, 4)
        vertex_5 = Vertex(self.mesh, 5)

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
        self.assertTrue((t[v] == values).all())

        #@todo: test delete: delete is not yet implemented in tag


    def test_types(self):
        # test with different types:

        # Ints
        t = IonTag('foo',3,'int', self.mesh)
        self.assertEqual(t._type, 'int')

        # Floats
        t = IonTag('foo',3,'float', self.mesh)
        self.assertEqual(t._type, 'float')


        # Complex
        t = IonTag('foo',3,'complex', self.mesh)
        self.assertEqual(t._type, 'complex')

        # String
        t = IonTag('foo',3,'string', self.mesh)
        self.assertEqual(t._type, 'string')

        # User defined

        # t = IonTag('foo',3,'user_defined', self.mesh)
#        self.assertEqual(t._type, 'user_defined')

        # Object
        t = IonTag('foo',3,'object', self.mesh)
        self.assertEqual(t._type, 'object')


    def test_iter(self):
        # test the iterator and verify that the correct type is passed back

        #------------------------------------------------------------
        # Initial step: Feed in values to the vertices in the mesh
        #------------------------------------------------------------

        t = IonTag('foo',1,'int', self.mesh)

        val = []
        x = 1

        for v in vertices(self.mesh):
            val.append(x)
            t[v] = val
            val.pop()
            x += 1

        #------------------------------------------------------------
        # Test the iteration over the tags
        #------------------------------------------------------------

        for key, item in t.iteritems():
            self.assertEqual(t[ key ], item  )


    def test_properties(self):
        # contains, len etc...
        pass

if __name__ == '__main__':
    unittest.main()

