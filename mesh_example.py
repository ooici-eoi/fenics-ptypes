__author__ = 'SChatterjee'

from dolfin import *
import numpy as np

def get_coord_array(ds,  lon_axis="", lat_axis="", z_axis=None):
    """
    Get the coordinate array

        @param ds netcdf dataset
        @param lon_axis type: str, description: longitudinal axis
        @param lat_axis type: str, description: latitude axis
        @param z_axis
        @retval coords, (x_cnt,y_cnt,z_cnt) type:tuple, description: coordinate array, shape

        """

def create_mesh(ds, outfile, topo_dim, geom_dim, x_coord, y_coord, z_coord):
    '''
    A method to create a mesh and store it in a specified file

        @param ds netcdf dataset
        @param outfile type: str, description: file to store mesh in
        @param topo_dim description: the topological dimension
        @param geom_dim description: the geometric dimension
        @param x_coord type: numpy array, description: array for x_coord (Ex: lon_rho)
        @param y_coord type: numpy array, description: array for y_coord (Ex: lat_rho)
        @param z_coord type: numpy array, description: array for z_coord (Ex: s_rho)

        @retval mesh

    '''


class MeshExample(object):
    """
    A helper class to facilitate the creation of a mesh of m x n vertices in a 2d grid, connected by segments.

    """

    def __init__(self, topo_dim, geom_dim):
        '''
        Initialize using topo_dim and geom_dim

        @param topo_dim topological dimension
        @param geom_dim geometric dimension

        '''

    def initializing_empty_grid(self, num_vertices, num_segments):
        '''
        Initialize an empty mesh

        @param num_vertices number of vertices
        @param num_segments number of segments

        '''

    def create_vertices(self, coords):
        """
        Create vertices

        @param coords is a 3 dimensional array

        """

    def create_cells(self, num_cells):
        '''
        Create cells

        @param num_cells number of cells

        '''

    def close(self):
        '''
        Close the editor used to create the mesh
        '''

class TimeMesh(object):
    """
    A mesh for time
    """

    def __init__(self):
        '''
        Create a new Mesh object for time and an editor for it

        '''


    def initializing_empty_grid(self, num_vertices, num_segments):
        '''
        Initialize an empty mesh
        '''

    def create_time_vertices(self, time_array):
        '''
        Create time vertices from the provided array of times
            @param time_array The array of time values as obtained from netcdf
        '''

    def create_time_cells(self, num_of_time_cells):
        '''
        Create time cells connecting successive time vertices from the first to the last one
            @param num_of_time_cells The number of time cells
        '''

    def close(self):
        '''
        Close the editor used to create the mesh
        '''


class TimeDomain(SubDomain):
    '''
    Defining a time domain
    '''
    def __init__(self, time_mesh, condition):
        '''
        Create a time domain

            @param time_mesh type: dolfin.mesh, description: The time mesh
            @param condition type: dict, description: Contains bounds in the form of keys in the dict
        '''

    def inside(self, x, on_boundary):
        '''
        A method that defines what the boundary of the time domain is
        '''

class Variable(object):
    '''
        A class that stores all the information that a variable object should have such as the name of the variable and
        the time array and the coordinates over which it is valid.
    '''

    def __init__(self, variable_name, time_array, coord_axes):
        '''
            @param variable_name The name of the variable (Ex: 'temp' or 'salt')
            @param time_array The array of time values
            @param coord_axes A MeshCoordinateAxes object
        '''

    def create_variable(self):
        '''
        Create a meshfunction for the variable
        '''

    def store_values(self, ds):
        '''
        Store values for that parameter from a dataset

            @param ds netcdf dataset
        '''


    def make_meshfunction_filename(self):
        '''
        Construct a name for the topological coordinate axes

        @ret-val the filename to store the meshfunction in
        '''

    def write_to_disk(self):
        '''
        Write the meshfunction for the variable to disk
        '''

class MeshCoordinateAxes(object):
    '''
        A class that stores all the information that a coordinate mesh topology should have such as the name of the
        coordinate mesh topology, the time domain over which it is valid and the time mesh that it is associated with.

     Connect a coordinate system with a time domain
    '''
    def __init__(self, name, time_domain, time_mesh, ds):
        '''
            @param name Name of the mesh topo (Ex: mesh_topo_1 --> (lon_rho, lat_rho, s_rho)
            @param time_domain Time Domain in which the mesh topo exists
            @param time_mesh The time mesh in which the mesh topo exists
            @param ds The netcdf dataset
        '''

    def create_mesh_topo(self, ds):
        '''
            Create a mesh object for the coordinate system.

            @param ds netcdf dataset
            @ret_val mesh_topo The mesh object
        '''

    def make_topo_filename(self):
        '''
        Construct a name for the topological coordinate axes

        @ret-val the filename to store the mesh
        '''



