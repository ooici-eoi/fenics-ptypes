#!/usr/bin/env python


from netCDF4 import Dataset
from dolfin import *
from pylab import *
import numpy as np
import numpy.ma as ma
from mesh_class_example import MeshExample

def get_coord_array(lon_axis="", lat_axis="", z_axis=None):
    x_coords=ds.variables[lon_axis][:]
    x_shp=x_coords.shape
    x_coords=x_coords.flatten()
    y_coords=ds.variables[lat_axis][:]
    y_shp=y_coords.shape
    y_coords=y_coords.flatten()

    x_cnt=x_shp[0]
    y_cnt=x_shp[1]

    if z_axis:
        z_coords=ds.variables[z_axis][:]
    else:
        z_coords=np.array([0])

    z_cnt=len(z_coords)
    zcol=np.empty([len(x_coords)])
    zcol.fill(z_coords[0])
    coords=np.column_stack([x_coords,y_coords,zcol])
    for z in xrange(z_cnt-1):
        zcol=np.empty([len(x_coords)])
        zcol.fill(z_coords[z+1])
        coords=np.vstack([coords,np.column_stack([x_coords,y_coords,zcol])])

    return coords, (x_cnt,y_cnt,z_cnt)

def create_mesh(outfile, topo_dim, geom_dim, x_coord, y_coord, z_coord):

    rho_coords, rho_shape = get_coord_array(x_coord, y_coord, z_coord)

    print rho_shape
    print len(rho_coords)

    mesh_example = MeshExample(topo_dim,geom_dim) # topo_dim = 1, geom_dim = 3
    num_vertices = len(rho_coords)
    num_cells = num_vertices

    mesh_example.initializing_empty_grid(num_vertices, num_cells)
    mesh_example.create_vertices(rho_coords)
    mesh_example.create_cells(num_cells)
    mesh_example.close()

    fx=File(outfile)
    fx << mesh_example.mesh

    return mesh_example.mesh
#------------------------------------------------------------------------------------------------
# Load and process the dataset
#------------------------------------------------------------------------------------------------

ds=Dataset("test_data/roms.nc")

#------------------------------------------------------------------------------------------------
# Write the meshes
#------------------------------------------------------------------------------------------------

# For mesh (lon_rho, lat_rho, s_rho)
mesh_topo_1 = create_mesh('test_data/outmesh_topo1.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_rho', y_coord = 'lat_rho', z_coord = 's_rho')

# TODO: Repeat for other meshes (i.e. (lon_u, lat_u, s_rho), etc)

# For mesh (lon_u, lat_u, s_rho)
#mesh_topo_2 = create_mesh('test_data/outmesh_topo2.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_u', y_coord = 'lat_u', z_coord = 's_rho')
#
## For mesh (lon_u, lat_u, s_rho)
#mesh_topo_3 = create_mesh('test_data/outmesh_topo3.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_v', y_coord = 'lat_v', z_coord = 's_rho')
#
## For mesh (lon_u, lat_u, s_rho)
#mesh_topo_4 = create_mesh('test_data/outmesh_topo4.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_rho', y_coord = 'lat_rho', z_coord = 's_w')

#------------------------------------------------------------------------------------------------
# Initialize Mesh Functions
#------------------------------------------------------------------------------------------------

temp = VertexFunction("double", mesh_topo_1)

#salt = VertexFunction("double", mesh_topo_1)



#temp = MeshFunction("double", mesh_topo_1, 0)
#
#salt = MeshFunction("double", mesh_topo_1, 0)
#
#u = MeshFunction("double", mesh_topo_2, 0)
#v = MeshFunction("double", mesh_topo_3, 0)
#w = MeshFunction("double", mesh_topo_4, 0)


#------------------------------------------------------------------------------------------------
# Put values into Mesh Functions
#------------------------------------------------------------------------------------------------
#a = ds.variables['temp'][0,:,:,:].flatten()

#var=ds.variables['temp']
#var.set_auto_maskandscale(True)
#a=var[0,:,:,:].flatten()
#
#temp.array()[:]  = a

# temp values
a = ds.variables['temp'][0,:,:,:].flatten()
temp.array()[:] = a

# salt values
#a  = ds.variables['salt'][0,:,:,:].flatten() # the key for salinity is salt?
#salt.array()[:] = a

# u values
#u.array()[:]  = ds.variables['u'][0,:,:,:].flatten()


#v.array()[:]  = ds.variables['v'][0,:,:,:].flatten()
#w.array()[:]  = ds.variables['w'][0,:,:,:].flatten()


#for v in vertices(mesh_topo_1):
#    print "values on vertices: %s" % salt[v]


#------------------------------------------------------------------------------------------------
# Saving Mesh Functions to disk
#------------------------------------------------------------------------------------------------

temp_outfile = File("test_data/temp_topo_1.xml")
temp_outfile << temp

#sal_outfile = File("test_data/sal_topo_1.bin")
#sal_outfile << salt


#------------------------------------------------------------------------------------------------
# Creating TIME: Creating a topo dim 1 and geom dim 1 mesh for time
#------------------------------------------------------------------------------------------------

#time_mesh =

