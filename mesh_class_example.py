
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

    def create_vertices(self, x_cnt, y_cnt, z_cnt):

        vertex_count = 0
        for z in xrange(0,z_cnt):
            for y in xrange(0,y_cnt):
                for x in xrange(0, x_cnt):
                        self.editor.add_vertex(vertex_count, x, y, z)
                        vertex_count += 1
        self.num_vertices = vertex_count

    def create_cells(self, num_cells):

        cell_cnt = 0
        for x in xrange(0,num_cells-1):
            self.editor.add_cell(cell_cnt,x, x+1)
            cell_cnt += 1

        # cyclically connect the last vertex with the first one
        self.editor.add_cell(cell_cnt, num_cells - 1, 0)

