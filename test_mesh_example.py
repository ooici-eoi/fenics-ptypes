
from netCDF4 import Dataset
import numpy as np
from pylab import *
import re
from dolfin import *
from mesh_class_example import MeshExample

#rho_coords = np.arange(750).reshape(10,15,5)

# TODO: Make Mesh from vertices (rho_coords)

mesh_example = MeshExample(1,3) # topo_dim = 1, geom_dim = 3

num_vertices = 750
num_segments = 1

mesh_example.initializing_empty_grid(num_vertices, num_segments)
mesh_example.create_vertices(10,15,5)

# make the cells
mesh_example.create_cells(num_segments)

fx=File('test_data/outmesh_topo1.xml')
fx << mesh_example.mesh

#fr = File('test_data/outmesh.raw')
#fr << mesh_example.mesh


# TODO: Repeat for other meshes (i.e. (lon_u, lat_u, s_rho), etc)
