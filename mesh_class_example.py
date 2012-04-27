
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
    rho_coords, rho_shape = get_coord_array(ds, x_coord, y_coord, z_coord)

    print "shape of mesh: ", rho_shape
    print "number of points in mesh: ", len(rho_coords)

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
        self.mesh = Mesh()
        self.editor = MeshEditor()
        self.editor.open(self.mesh, topo_dim, geom_dim) # topo_dim = 1, geom_dim = 2

    def initializing_empty_grid(self, num_vertices, num_segments):
        '''
        Initialize an empty mesh

        @param num_vertices number of vertices
        @param num_segments number of segments

        '''
        self.editor.init_vertices(num_vertices)
        self.editor.init_cells(num_segments) # initializing the segments

    def create_vertices(self, coords):
        """
        Create vertices

        @param coords is a 3 dimensional array

        """
        i=0
        for x in coords:
            self.editor.add_vertex(i, x[0],x[1],x[2])
            i +=1

    def create_cells(self, num_cells):
        '''
        Create cells

        @param num_cells number of cells

        '''
        cell_cnt = 0
        for x in xrange(num_cells):
            self.editor.add_cell(cell_cnt,x, x)
            cell_cnt += 1

    def close(self):
        '''
        Close the editor used to create the mesh
        '''
        self.editor.close()

class TimeMesh(object):
    """
    A mesh for time
    """

    def __init__(self):
        '''
        Create a new Mesh object for time and an editor for it

        '''
        self.mesh = Mesh()
        self.editor = MeshEditor()
        self.editor.open(self.mesh, 1, 1) # topo_dim = 1, geom_dim = 1

        self.last_unique_subdomain_value = 1

    def initializing_empty_grid(self, num_vertices, num_segments):
        '''
        Initialize an empty mesh
        '''
        self.editor.init_vertices(num_vertices)
        self.editor.init_cells(num_segments) # initializing the segments

    def create_time_vertices(self, time_array):
        '''
        Create time vertices from the provided array of times
            @param time_array The array of time values as obtained from netcdf
        '''
        i=0
        for x in time_array:
            self.editor.add_vertex(i, float(x)) # seems that fenics does not like numpy.float but likes python float
            i +=1

    def create_time_cells(self, num_of_time_cells):
        '''
        Create time cells connecting successive time vertices from the first to the last one
            @param num_of_time_cells The number of time cells
        '''
        cell_cnt = 0
        for x in xrange(num_of_time_cells-1):
            self.editor.add_cell(cell_cnt,x, x+1)
            cell_cnt += 1

    def close(self):
        '''
        Close the editor used to create the mesh
        '''
        self.editor.close()

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
        self.unique_value = time_mesh.last_unique_subdomain_value
        time_mesh.last_unique_subdomain_value += 1

        self.lower_bound = condition['lower_bound']
        self.upper_bound = condition['upper_bound']

        SubDomain.__init__(self)

    def inside(self, x, on_boundary):
        '''
        A method that defines what the boundary of the time domain is
        '''
        return True if self.lower_bound <= x[0] and  x[0] <= self.upper_bound else False


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
        self.name = variable_name
        self.time_array = time_array
        self.time_mesh = coord_axes.time_mesh
        self.mesh_topo = coord_axes.mesh_topo

        self.create_variable()

    def create_variable(self):
        '''
        Create a meshfunction for the variable
        '''
        self.variable_handle = MeshFunction("double", self.mesh_topo, 1)

    def store_values(self, ds):
        '''
        Store values for that parameter from a dataset
        '''
        self.values = ds.variables[self.name][0,:,:,:].flatten()
        self.variable_handle.array()[:] = self.values

    def make_meshfunction_filename(self):
        '''
        Construct a name for the topological coordinate axes
        '''
        name = self.name
        return name

    def write_to_disk(self):
        '''
        Write the meshfunction for the variable to disk
        '''
        temp_outfile = File('test_data/' + self.make_meshfunction_filename() + '.xml')
        temp_outfile << self.variable_handle

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
        self.name = name
        self.time_domain = time_domain
        self.time_mesh = time_mesh

        if self.name == 'mesh_topo_1':
            self.x_coord = 'lon_rho'
            self.y_coord = 'lat_rho'
            self.z_coord = 's_rho'
        elif self.name == 'mesh_topo_2':
            self.x_coord = 'lon_u'
            self.y_coord = 'lat_u'
            self.z_coord = 's_rho'
        elif self.name == 'mesh_topo_3':
            self.x_coord = 'lon_v'
            self.y_coord = 'lat_v'
            self.z_coord = 's_rho'
        elif self.name == 'mesh_topo_4':
            self.x_coord = 'lon_rho'
            self.y_coord = 'lat_rho'
            self.z_coord = 's_w'

        self.mesh_topo = self.create_mesh_topo(ds)

    def create_mesh_topo(self, ds):
        '''
            Create a mesh object for the coordinate system.

            @param ds netcdf dataset
            @ret_val mesh_topo The mesh object
        '''

        # invoking the function below creates a mesh and also writes it to a disk
        mesh_topo = create_mesh(ds, 'test_data/' + self.make_topo_filename() + '.xml',
                                    topo_dim = 1, geom_dim = 3, 
                                    x_coord = self.x_coord, 
                                    y_coord = self.y_coord, 
                                    z_coord = self.z_coord)
        return mesh_topo

    def make_topo_filename(self):
        '''
        Construct a name for the topological coordinate axes

        @ret-val the filename to store the mesh
        '''
        name = self.name + '_' + str(self.time_domain.unique_value)
        return name


