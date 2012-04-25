
from dolfin import *

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
