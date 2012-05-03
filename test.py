#!/usr/bin/env python

__author__ = 'SChatterjee'

from dolfin import *
import numpy as np

print "Initialize an empty mesh"
mesh=Mesh()
print "Instantiate a MeshEditor with topo-dim=1 and geom-dim=1 (for timeline)"
editor=MeshEditor()
editor.open(mesh,1,1)
print "Initialize 3 vertices and 2 cells"
editor.init_vertices(3)
editor.init_cells(2)
print "Add 3 vertices"
editor.add_vertex(0,11)
editor.add_vertex(1,22)
editor.add_vertex(2,33)
print "Add 2 cells"
editor.add_cell(0,0,1)
editor.add_cell(1,1,2)
print "Close the editor"
editor.close()

print "Write the mesh"
f=File('outmesh.xml')
f << mesh
f=None

print "Make a MeshFunction (timedata)"
times=MeshFunction("int",mesh,0)
print "Assign temporal data to time vertices"
times.array()[:]=np.array([1251325,1251379,1251421],dtype='int')
print "Write the temporal function (data)"
f=File('tdata.xml')
f << times
f=None