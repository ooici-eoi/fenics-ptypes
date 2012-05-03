__author__ = 'SChatterjee'

from dolfin import *
import numpy

#--------------------------------------------------------------------------------------------
# One can create a vector.... and also a matrix and a general tensor
#--------------------------------------------------------------------------------------------

# Create a vector of size 10
x = Vector(10)

# Assigning vlaues to a vector

a = numpy.array([1221, 123.32, 23213, 343,3.34234, 34.3434]) # putting in double because
v = Vector(a.size)
v.set_local(a) # this assigns the values to the vector

# To read off the values in v
print "Values in v:", v.array()

#--------------------------------------------------------------------------------------------
# One can also create functions on VectorFunctionSpace 's that are vector valued
# For documentation please check:
# http://fossies.org/unix/privat/dolfin-1.0.0.tar.gz/dox/classdolfin_1_1functions_1_1functionspace_1_1VectorFunctionSpace.html
#
#--------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------
# Creating a mesh without specifying the geometrical coordinates (topo_dim = 1, geom_dim = 1)
#--------------------------------------------------------------------------------------------


mesh = Mesh()
editor = MeshEditor()
editor.open(mesh, 1, 1) # topo_dim = 1, geom dim = 1

editor.init_vertices(6)
editor.init_cells(3)



vertex_0 = Vertex(mesh, 0)
vertex_1 = Vertex(mesh, 1)
vertex_2 = Vertex(mesh, 2)
vertex_3 = Vertex(mesh, 3)
vertex_4 = Vertex(mesh, 4)
vertex_5 = Vertex(mesh, 5)

editor.add_cell(0,0,1)
editor.add_cell(1,1,2)
editor.add_cell(2,2,3)
#editor.add_cell(3,3,4)
#editor.add_cell(4,4,5)


mesh.order()

V = VectorFunctionSpace(mesh, "Lagrange", 1)

#-----
# One can now choose several kinds of functions on this VectorFunctionSpace... page 23 of manual

# Function..... page 110 of manual
w = Function(V)
u = Function(V)

# to see the array of values being held by it
print w.vector().array()
print u.vector().array()
# one can calculate inner products of the vectors
print inner(w, u)

# this concept of inner product means that w and v are vectors and not scalars

a = numpy.array([1221, 123.32, 23213, 343,3.34234]) # putting in double because
w.vector()[:] = a

print w.vector().array()




##---------------------------------------------------------------------------------------
## This section below does not define vector valued functions
## Instead it copies the values in stored in a vector, vector.array(), and writes them
## to all the vertices in the mesh... and so vector.array.size() should be equal to
## mesh.num_vertices()
##---------------------------------------------------------------------------------------
#
#f = Function(V)
#
#vec = f.vector()
#
#for i in xrange(a.size):
#    vec[i] = a[i]
#
## or you can do
#f.vector()[:] = a
#
## now we can read off the values assigned to the function
#
## using a different handle
#vec2 = f.vector()
#print "Values in f: ", vec2.array()






