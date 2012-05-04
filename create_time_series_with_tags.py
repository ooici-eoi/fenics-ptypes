__author__ = 'SChatterjee'


from dolfin import *
from tag import IonTag
import random

mesh = Mesh()
editor = MeshEditor()
editor.open(mesh, 1, 1) # topo_dim = 1, geom dim = 1

editor.init_vertices(4)
editor.init_cells(3)

#--------------------------------------------------------------------------------------------
# Create time vertices
#--------------------------------------------------------------------------------------------

vertex_0 = Vertex(mesh, 0)
vertex_1 = Vertex(mesh, 1)
vertex_2 = Vertex(mesh, 2)
vertex_3 = Vertex(mesh, 3)

#--------------------------------------------------------------------------------------------
# Create segments connecting the vertices
#--------------------------------------------------------------------------------------------

editor.add_cell(0,0,1)
editor.add_cell(1,1,2)

editor.close()

#--------------------------------------------------------------------------------------------
# Create tags
#--------------------------------------------------------------------------------------------

# tag1
t1 = IonTag('foo',2,'int', mesh)

# now put random values to the tag

for v in vertices(mesh):
    values = [random.randint(1,10), random.randint(10,20), random.randint(20,30),random.randint(30,40) ]
    t1[v] = values

# tag2
t2 = IonTag('foo',2,'float', mesh)

# now put random values to the tag

for v in vertices(mesh):
    values = [random.randint(1,10), random.randint(10,20), random.randint(20,30)]
    t2[v] = values

#--------------------------------------------------------------------------------------------
# Check values in the tags
#--------------------------------------------------------------------------------------------

# print values for tag, t1, for all the vertices in the mesh

print "vertices, t1[v] ----->"
print ""

for v in vertices(mesh):
    print v, t1[v]

# print the _entity_values dictionary held by tag, t1

print ""
print "t1._entity_values --> ", t1._entity_values
print ""

# print values for tag, t2, for all the vertices in the mesh

print "vertices, t2[v] ----->"
print ""
for v in vertices(mesh):
    print v, t2._entity_values

# print the _entity_values dictionary held by tag, t2

print ""
print "t2._entity_values --> ", t2._entity_values
print ""





