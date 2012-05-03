#!/usr/bin/env python

__author__ = 'SChatterjee'

from netCDF4 import Dataset
from dolfin import *
from pylab import *
import numpy as np
from mesh_class_example import MeshExample, TimeMesh, TimeDomain

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
# Creating TIME: Creating a topo dim 1 and geom dim 1 mesh for time
#------------------------------------------------------------------------------------------------

time_mesh = TimeMesh()

# for now we look at only one spatial point
time_array = ds.variables['ocean_time'][:].flatten()

num_of_time_vertices = len(time_array)

time_mesh.initializing_empty_grid(num_vertices=num_of_time_vertices, num_segments= num_of_time_vertices-1)
time_mesh.create_time_vertices(time_array)
time_mesh.create_time_cells(num_of_time_cells=num_of_time_vertices)

time_out = File("test_data/time_mesh1.xml")
time_out << time_mesh.mesh


#------------------------------------------------------------------------------------------------
# Connecting the time mesh to the topo mesh
#------------------------------------------------------------------------------------------------

def make_topo_name(topo_coordinate_name, timedomain_unique_value):
    '''
    Construct a name for the topological coordinate axes
    '''
    name = topo_coordinate_name + '_' + str(timedomain_unique_value)
    return name



#------------------------------------------------------------------------------------------------
# Connecting the time mesh to the mesh functions for variables (temp, sal etc)
#------------------------------------------------------------------------------------------------

def make_meshfunction_name(variable_name, time_vertex_index):
    '''
    Construct a name for the topological coordinate axes
    '''
    name = variable_name + '_' + str(time_vertex_index)
    return name


#------------------------------------------------------------------------------------------------
# Creating subdomains on the time mesh by marking them using meshfunctions
#------------------------------------------------------------------------------------------------


# Mark a subdomain on the time mesh with a value

condition = {'lower_bound' : 0, 'upper_bound' : 10**9}
time_domain_0 = TimeDomain(time_mesh, condition)
subdomain_func_0 = MeshFunction("uint", time_mesh.mesh, 0)
subdomain_func_0.set_all(0)
time_domain_0.mark(subdomain_func_0, time_domain_0.unique_value)

# Mark another subdomain on the time mesh with a value

condition = {'lower_bound' : 2, 'upper_bound' : 1.95220800*(10**8) }
time_domain_1 = TimeDomain(time_mesh, condition)
subdomain_func_1 = MeshFunction("uint", time_mesh.mesh, 0)
subdomain_func_1.set_all(0)
time_domain_1.mark(subdomain_func_1, time_domain_1.unique_value)


#------------------------------------------------------------------------------------------------
# Connecting coordinate-axes-topologies with the time mesh
#------------------------------------------------------------------------------------------------

mesh_filename_1 = make_topo_name(topo_coordinate_name = 'mesh_topo_1', timedomain_unique_value = time_domain_0.unique_value)
mesh_filename_2 = make_topo_name(topo_coordinate_name = 'mesh_topo_2', timedomain_unique_value = time_domain_1.unique_value)
mesh_filename_3 = make_topo_name(topo_coordinate_name = 'mesh_topo_3', timedomain_unique_value = time_domain_0.unique_value)
mesh_filename_4 = make_topo_name(topo_coordinate_name = 'mesh_topo_4', timedomain_unique_value = time_domain_1.unique_value)

#------------------------------------------------------------------------------------------------
# Connecting variables with the time mesh
#------------------------------------------------------------------------------------------------

temp_filename = make_meshfunction_name(variable_name = 'temp', time_vertex_index = 1)
salt_filename = make_meshfunction_name(variable_name = 'salt', time_vertex_index = 1)
u_filename = make_meshfunction_name(variable_name = 'u', time_vertex_index = 1)
v_filename = make_meshfunction_name(variable_name = 'v', time_vertex_index = 1)
w_filename = make_meshfunction_name(variable_name = 'w', time_vertex_index = 1)

#------------------------------------------------------------------------------------------------
# Write the meshes
#------------------------------------------------------------------------------------------------

# For mesh (lon_rho, lat_rho, s_rho)
mesh_topo_1 = create_mesh('test_data/' + mesh_filename_1 + '.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_rho', y_coord = 'lat_rho', z_coord = 's_rho')

# TODO: Repeat for other meshes (i.e. (lon_u, lat_u, s_rho), etc)

# For mesh (lon_u, lat_u, s_rho)
mesh_topo_2 = create_mesh('test_data/' + mesh_filename_2 + '.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_u', y_coord = 'lat_u', z_coord = 's_rho')

# For mesh (lon_u, lat_u, s_rho)
mesh_topo_3 = create_mesh('test_data/' + mesh_filename_3 + '.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_v', y_coord = 'lat_v', z_coord = 's_rho')

# For mesh (lon_u, lat_u, s_rho)
mesh_topo_4 = create_mesh('test_data/' + mesh_filename_4 + '.xml', topo_dim = 1, geom_dim = 3, x_coord = 'lon_rho', y_coord = 'lat_rho', z_coord = 's_w')

#------------------------------------------------------------------------------------------------
# Initialize Mesh Functions
#------------------------------------------------------------------------------------------------

temp = MeshFunction("double", mesh_topo_1, 0)
salt = MeshFunction("double", mesh_topo_1, 0)
u = MeshFunction("double", mesh_topo_2, 0)
v = MeshFunction("double", mesh_topo_3, 0)
w = MeshFunction("double", mesh_topo_4, 0)

#------------------------------------------------------------------------------------------------
# Put values into Mesh Functions
#------------------------------------------------------------------------------------------------

# temp values
temp.array()[:] = ds.variables['temp'][0,:,:,:].flatten()

# salt values
salt.array()[:] = ds.variables['salt'][0,:,:,:].flatten() # the key for salinity is salt?

# u values
u.array()[:]  = ds.variables['u'][0,:,:,:].flatten()

# v values
v.array()[:]  = ds.variables['v'][0,:,:,:].flatten()

# w values
w.array()[:]  = ds.variables['w'][0,:,:,:].flatten()

#------------------------------------------------------------------------------------------------
# Saving Mesh Functions to disk
#------------------------------------------------------------------------------------------------

temp_outfile = File('test_data/' + temp_filename + '.xml')
temp_outfile << temp

salt_outfile = File('test_data/' + salt_filename + '.xml')
salt_outfile << salt

u_outfile = File('test_data/' + u_filename + '.xml')
u_outfile << u

v_outfile = File('test_data/' + v_filename + '.xml')
v_outfile << v

w_outfile = File('test_data/' + w_filename + '.xml')
w_outfile << w







