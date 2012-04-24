#!/usr/bin/env python

from dolfin import *
import numpy as np

print "Initialize an empty mesh"
mesh=Mesh()
print "Instantiate a MeshEditor with topo-dim=2 and geom-dim=3 (for timeline)"
editor=MeshEditor()
editor.open(mesh,2,3)
print "Initialize 3 vertices and 2 cells"
editor.init_vertices(3)
editor.init_cells(1)
print "Add 3 vertices"
editor.add_vertex(0,0,0,0)
editor.add_vertex(1,0,1,0)
editor.add_vertex(2,1,1,1)
print "Add 1 cell"
editor.add_cell(0,0,1,2)
print "Close the editor"
editor.close()

print "Write the mesh"
f=File('outmesh_2.xml')
f << mesh
f=None

# print "Make a MeshFunction (timedata)"
# times=MeshFunction("int",mesh,0)
# print "Assign temporal data to time vertices"
# times.array()[:]=np.array([1251325,1251379,1251421],dtype='int')
# print "Write the temporal function (data)"
# f=File('tdata_2.xml')
# f << times
# f=None