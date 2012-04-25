
from dolfin import *
from test_mesh_roms import get_coord_array, create_mesh

class MeshExample(object):
    """
    A mesh with m x n vertices in a 2d grid, connected by segments. The vertices
    are ordered from 0 to (m * n -1). The edges are also ordered:

    Ex: For m = 4, n = 3, the meshes are ordered as:

     0 1 2 3
     4 5 6 7
     8 9 10 11

    The edges are ordered as

    * 0 * 1 * 2 *
    3   4   5   6
    * 7 * 8 * 9 *

    """
    def __init__(self, topo_dim, geom_dim):

        self.mesh = Mesh()
        self.editor = MeshEditor()
        self.editor.open(self.mesh, topo_dim, geom_dim) # topo_dim = 1, geom_dim = 2

    def initializing_empty_grid(self, num_vertices, num_segments):

        self.editor.init_vertices(num_vertices)
        self.editor.init_cells(num_segments) # initializing the segments

    def create_vertices(self, coords):
        """
        coords is a 3 dimensional array
        """
        i=0
        for x in coords:
            self.editor.add_vertex(i, x[0],x[1],x[2])
            i +=1

    def create_cells(self, num_cells):

        cell_cnt = 0
        for x in xrange(num_cells):
            self.editor.add_cell(cell_cnt,x, x)
            cell_cnt += 1

    def close(self):
        self.editor.close()

class TimeMesh(object):
    """
    A mesh for time
    """

    def __init__(self):

        self.mesh = Mesh()
        self.editor = MeshEditor()
        self.editor.open(self.mesh, 1, 1) # topo_dim = 1, geom_dim = 1

        self.last_unique_subdomain_value = 0

    def initializing_empty_grid(self, num_vertices, num_segments):

        self.editor.init_vertices(num_vertices)
        self.editor.init_cells(num_segments) # initializing the segments

    def create_time_vertices(self, time_array):
        '''
        Create time vertices from the provided array of times
        '''
        i=0
        for x in time_array:
            self.editor.add_vertex(i, float(x)) # seems that fenics does not like numpy.float but likes python float
            i +=1

    def create_time_cells(self, num_of_time_cells):
        '''
        Create time cells connecting successive time vertices from the first to the last one
        '''
        cell_cnt = 0
        for x in xrange(num_of_time_cells-1):
            self.editor.add_cell(cell_cnt,x, x+1)
            cell_cnt += 1

    def close(self):
        self.editor.close()

class TimeDomain(SubDomain):
    '''
    Defining a time domain
    '''
    def __init__(self, time_mesh, condition):
        self.unique_value = time_mesh.last_unique_subdomain_value
        time_mesh.last_unique_subdomain_value += 1

        self.lower_bound = condition['lower_bound']
        self.upper_bound = condition['upper_bound']

        SubDomain.__init__(self)

    def inside(self, x, on_boundary):
        return True if self.lower_bound <= x[0] and  x[0] <= self.upper_bound else False


class Variable(object):
    '''
    Connect a variable to a time vertex
    '''

    def __init__(self, variable_name, time_vertex_index, mesh_topo):
        self.name = variable_name
        self.time_vertex_index = time_vertex_index
        self.time_mesh = mesh_topo.time_mesh
        self.mesh_topo = mesh_topo

    def create_variable(self):
        self.filename = self.make_meshfunction_filename(self.name, self.time_vertex_index)
        self.variable_handle = MeshFunction("double", self.mesh_topo, 0)
        return self.variable_handle

    def store_values(self, ds):
        '''
        Store values for that variable from a dataset
        '''
        self.variable_handle.array()[:] = ds.variables[self.name][0,:,:,:].flatten()

    def make_meshfunction_filename(self):
        '''
        Construct a name for the topological coordinate axes
        '''
        name = self.name + '_' + str(self.time_vertex_index)
        return name

    def write_to_disk(self):
        temp_outfile = File('test_data/' + self.filename + '.xml')
        temp_outfile << self.variable_handle

def MeshCoordinateAxes(object):
    '''
    Connects a coordinate system with a time domain
    '''
    def __init__(self, name, time_domain, time_mesh):
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

    def create_mesh_topo(self):

        # invoking the function below creates a mesh and writes it to a disk also
        mesh_topo = create_mesh('test_data/' + self.make_topo_filename() + '.xml',
                                    topo_dim = 1, geom_dim = 3, 
                                    x_coord = self.x_coord, 
                                    y_coord = self.y_coord, 
                                    z_coord = self.z_coord)

        return mesh_topo

    def make_topo_filename(self):
        '''
        Construct a name for the topological coordinate axes
        '''
        name = self.name + '_' + str(self.time_domain.unique_value)
        return name


