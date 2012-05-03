__author__ = 'SChatterjee'

from dolfin import *
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

#--------------------------------------------------------------------------------------------
# Check that the iterators are working
#--------------------------------------------------------------------------------------------

print "Printing mesh entities by iterating....."
for c in cells(mesh):
    for v0 in vertices(c):
        print c, v0

"""
#--------------------------------------------------------------------------------------------
# Creating another mesh, topo_dim =1, geom_dim = 1
#--------------------------------------------------------------------------------------------


mesh = Mesh()
editor = MeshEditor()
editor.open(mesh, 1, 1) # topo_dim = 1, geom dim = 1

editor.init_vertices(6)
editor.init_cells(6)



vertex_0 = Vertex(mesh, 0)
vertex_1 = Vertex(mesh, 1)
vertex_2 = Vertex(mesh, 2)
vertex_3 = Vertex(mesh, 3)
vertex_4 = Vertex(mesh, 4)
vertex_5 = Vertex(mesh, 5)

editor.add_cell(0,0,1)
editor.add_cell(1,1,2)
editor.add_cell(2,2,3)
editor.add_cell(3,3,4)
editor.add_cell(4,4,5)

#--------------------------------------------------------------------------------------------
# Check that the iterators are working
#--------------------------------------------------------------------------------------------

print "Printing mesh entities by iterating....."
for c in cells(mesh):
    for v0 in vertices(c):
        print v0
"""