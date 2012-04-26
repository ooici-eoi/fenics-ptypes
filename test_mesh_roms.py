#!/usr/bin/env python


from netCDF4 import Dataset
from dolfin import *
from pylab import *
import numpy as np
from mesh_class_example import MeshExample, TimeMesh, TimeDomain, Parameter, MeshCoordinateAxes

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

    print "shape of mesh: %s" % rho_shape
    print "number of points in mesh %s" % len(rho_coords)

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

time_out = File("test_data/time_mesh.xml")
time_out << time_mesh.mesh

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
# Create the MeshCoordinateAxes objects that contain the topo meshes and information about
# which time domains they are for
#------------------------------------------------------------------------------------------------

# For mesh (lon_rho, lat_rho, s_rho)
coord_axes_1 = MeshCoordinateAxes(  name = 'mesh_topo_1',
                                    time_domain = time_domain_0,
                                    time_mesh = time_mesh,
                                    ds = ds)
mesh_topo_1 = coord_axes_1.mesh_topo

# For mesh (lon_u, lat_u, s_rho)
coord_axes_2 = MeshCoordinateAxes(  name = 'mesh_topo_2',
                                    time_domain = time_domain_0,
                                    time_mesh = time_mesh,
                                    ds = ds)
mesh_topo_2 = coord_axes_2.mesh_topo

# For mesh (lon_u, lat_u, s_rho)
coord_axes_3 = MeshCoordinateAxes(  name = 'mesh_topo_3',
                                    time_domain = time_domain_0,
                                    time_mesh = time_mesh,
                                    ds = ds)
mesh_topo_3 = coord_axes_3.mesh_topo

# For mesh (lon_u, lat_u, s_rho)
coord_axes_4 = MeshCoordinateAxes(  name = 'mesh_topo_4',
                                    time_domain = time_domain_0,
                                    time_mesh = time_mesh,
                                    ds = ds)
mesh_topo_4 = coord_axes_4.mesh_topo

#------------------------------------------------------------------------------------------------
# Create Parameter objects which create appropriate mesh functions and connect them with their
# corresponding time vertices and mesh topologies
#------------------------------------------------------------------------------------------------

#temp = Parameter(parameter_name='temp', time_vertex_index= 1, coord_axes=coord_axes_1)
#salt = Parameter(parameter_name='salt', time_vertex_index= 1, coord_axes=coord_axes_1)
#u = Parameter(parameter_name='u', time_vertex_index= 1, coord_axes=coord_axes_2)
#v = Parameter(parameter_name='v', time_vertex_index= 1, coord_axes=coord_axes_3)
#w = Parameter(parameter_name='w', time_vertex_index= 1, coord_axes=coord_axes_4)


# A parameter is defined over a mesh (a coordinate_axes mesh such as (lon_rho,lat_rho,s_rho))
# and a sequence of times (this is provided by the time_mesh)

temp = Parameter(parameter_name='temp', time_array = time_array, coord_axes=coord_axes_1)
salt = Parameter(parameter_name='salt', time_array = time_array, coord_axes=coord_axes_1)
u = Parameter(parameter_name='u', time_array = time_array, coord_axes=coord_axes_2)
v = Parameter(parameter_name='v', time_array = time_array, coord_axes=coord_axes_3)
w = Parameter(parameter_name='w', time_array = time_array, coord_axes=coord_axes_4)


#------------------------------------------------------------------------------------------------
# Transfer values from a netCDF dataset to the Parameter objects...
# After transferring, we can access the data transferred using either values attribute of
# the Parameter object: Parameter.values --> returns a masked array....
# or from the meshfunction handle of the Parameter object:
# Parameter.parameter_handle.array() --> returns a numpy array
#------------------------------------------------------------------------------------------------

# temp values
temp.store_values(ds)
# salt values
salt.store_values(ds)
# u values
u.store_values(ds)
# v values
v.store_values(ds)
# w values
w.store_values(ds)

#------------------------------------------------------------------------------------------------
# Saving Mesh Functions to disk
#------------------------------------------------------------------------------------------------

temp.write_to_disk()
salt.write_to_disk()
u.write_to_disk()
v.write_to_disk()
w.write_to_disk()


#------------------------------------------------------------------------------------------------
# Print the values stored in the meshfunctions, subdomain_func_0 and subdomain_func_1,
# which store specified values on their respective time domains and 0s for the rest
# of the time vertices
#------------------------------------------------------------------------------------------------

print "time_array (ocean_time): %s" % time_array
print "ds.variables['ocean_time'][:] --> %s" % ds.variables['ocean_time'][:]

print "The subdomain function 0 has the following values over its time_mesh: %s" % subdomain_func_0.array()
print "The subdomain function 0 has the following values over its time_mesh: %s" % subdomain_func_1.array()

# print the vertex index for which a particular temp value is valid
print "Values associated with parameter, temp (masked array): %s" % temp.values

