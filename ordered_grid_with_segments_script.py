
from dolfin import *
from ordered_grid_with_segments import MeshExample

num_rows = 3 # number of rows
num_columns = 4 # number of columns

mesh_example = MeshExample()

mesh_example.initializing_empty_grid(num_rows, num_columns)

mesh_example.create_vertices(num_rows, num_columns)

mesh_example.create_segments(num_rows, num_columns)

#-------------
#
# Visualization:
#
# to print number of vertices created
#-------------
print "number of vertices: %s" % mesh_example.mesh.num_entities(0)
print "number of segments: %s" % mesh_example.mesh.num_entities(1)

# to print in order to see the ordering of the segments and the vertices
for c in cells(mesh_example.mesh): # iterates over the segments
    print c# the segment
    for v in vertices(c):
        print v # the vertices associated with the segment

    print "\n"

#---------------------------------------
# cell functions
#---------------------------------------

cfunc = CellFunction("uint", mesh_example.mesh)

ctr = 0
for cell in cells(mesh_example.mesh):
    cfunc[cell] = ctr
    ctr += 1

# to check that the cell function works
for cell in cells(mesh_example.mesh):
    print "values on cell: %s" % cfunc[cell]

#---------------------------------------
# vertex functions
#---------------------------------------

# writing on top of vertices
vfunc = VertexFunction("uint", mesh_example.mesh)

ctr = 0
for v in vertices(mesh_example.mesh):
    vfunc[v] = 100 + ctr
    ctr += 1

for v in vertices(mesh_example.mesh):
    print "values on vertices: %s" % vfunc[v]

#-----------------------------------------------------
# Creating subdomain using fenics subdomain class
#-----------------------------------------------------

from ordered_grid_with_segments import SubDomain0

subdomain = SubDomain0()

subdomain_func = MeshFunction('uint', mesh_example.mesh, 0)

subdomain_func.set_all(0)

subdomain.mark(subdomain_func, 10)

subdomain_func.array()


#-------------------------------------------------------------------
# Creating contiguous blobs without using Contiguous_Blob class
#-------------------------------------------------------------------

from ordered_grid_with_segments import Contiguous_Blob

quad = Contiguous_Blob(mesh_example.mesh, [0,1,4,5])

for v in vertices(mesh_example.mesh):
    print "Is vertex %s inside quad? %s" %(v, quad.inside(v))











