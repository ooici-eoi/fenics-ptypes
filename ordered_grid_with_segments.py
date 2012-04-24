
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
    4   5   6   7
    * 8 * 9 * 10*

    """
    def __init__(self):

        self.mesh = Mesh()
        self.editor = MeshEditor()
        self.editor.open(self.mesh, 1, 2) # topo_dim = 1, geom_dim = 2

    def initializing_empty_grid(self, num_rows, num_columns):


        num_vertices = num_columns * num_rows
        num_segments = 2 * num_columns * num_rows - num_columns - num_rows

        self.editor.init_vertices(num_vertices)
        self.editor.init_cells(num_segments) # initializing the segments

    def create_vertices(self, num_rows, num_columns):

        vertex_count = 0
        for y in xrange(0,num_rows):
            for x in xrange(0,num_columns):
                self.editor.add_vertex(vertex_count, x, y)
                vertex_count += 1

    def create_segments(self, num_rows, num_columns):

        seg_ct = 0

        for row in xrange(0,num_rows):

            for x in xrange(row * num_columns, (row + 1)* num_columns - 1):
                self.editor.add_cell(seg_ct,x, x+1) # horizontal segments
                seg_ct += 1
            if row < num_rows - 1:
                for x in xrange(row * num_columns, (row + 1)* num_columns):
                    self.editor.add_cell(seg_ct, x, x + num_columns)
                    seg_ct += 1


class Contiguous_Blob(object):
    def __init__(self, mesh, list_of_vertex_numbers = []):

        self.mesh = mesh

        list_of_vertices = []
        for num in list_of_vertex_numbers:
            vertex = MeshEntity(self.mesh, 0, num)
            list_of_vertices.append(vertex)

#        self.check_contiguity(list_of_vertices)

        self.subdomain = VertexFunction("bool", self.mesh)
        self.subdomain.set_all(False)

        for vertex in vertices(mesh):
            if vertex in list_of_vertices:
                self.subdomain[vertex] = True

    def check_contiguity(self, list_of_vertices):
        """
        helper method to check that the vertices making up the
        """

        for v0 in list_of_vertices:
            vertex_neighbors = []
            for v in vertices(v0):
                vertex_neighbors.append(v)
            intersect = [val for val in list_of_vertices if val in vertex_neighbors]
            if len(intersect) == 0:
                raise AssertionError('The vertices chosen should be contiguous')

    def inside(self, vertex):
        """
        Returns true of the cell is inside the Quadrilater
        """
        return self.subdomain[vertex]


class SubDomain0(SubDomain):
    def inside(self, x, on_boundary):
        return True if x[1] <= 1 else False

