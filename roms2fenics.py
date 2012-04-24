#!/usr/bin/env python


from netCDF4 import Dataset
import numpy as np
from pylab import *
import re
from dolfin import *


def get_coord_array(lon_axis="", lat_axis="", z_axis=None):
#    x_coords=ds.variables[lon_axis][:]
#    x_shp=x_coords.shape
#    x_coords=x_coords.flatten()
#    y_coords=ds.variables[lat_axis][:]
#    y_shp=y_coords.shape
#    y_coords=y_coords.flatten()
#
#    x_cnt=x_shp[0]
#    y_cnt=x_shp[1]
#
#    if z_axis:
#        z_coords=ds.variables[z_axis][:]
#    else:
#        z_coords=np.array([0])
#
#    z_cnt=len(z_coords)
#    zcol=np.empty([len(x_coords)])
#    zcol.fill(z_coords[0])
#    coords=np.column_stack([x_coords,y_coords,zcol])
#    for z in xrange(z_cnt-1):
#        zcol=np.empty([len(x_coords)])
#        zcol.fill(z_coords[z+1])
#        coords=np.vstack([coords,np.column_stack([x_coords,y_coords,zcol])])
#

    ## Shortcut test
    coords=np.array([[0,0,0],[1,0,0],[2,0,0],[0,1,0],[1,1,0],[2,1,0],[0,2,0],[1,2,0],[2,2,0]],dtype='double')
    x_cnt=3
    y_cnt=3
    z_cnt=1

    return coords, (x_cnt,y_cnt,z_cnt)

# Load and process the dataset
ds=Dataset("test_data/roms.nc")

rho_coords, rho_shape = get_coord_array('lon_rho', 'lat_rho', 's_rho')

print rho_shape
print len(rho_coords)

# TODO: Make Mesh from vertices (rho_coords)
mesh = Mesh()
editor = MeshEditor()
editor.open(mesh,1,3)
editor.init_vertices(len(rho_coords))
editor.init_cells(1)
i=0
for x in rho_coords:
#    print x
    editor.add_vertex(i, x[0],x[1],x[2])
    i+=1

editor.add_cell(0,0,0)

editor.close()
fx=File('test_data/outmesh.xml')
fx << mesh

#fr = File('test_data/outmesh.raw')
#fr << mesh


# TODO: Repeat for other meshes (i.e. (lon_u, lat_u, s_rho), etc)
