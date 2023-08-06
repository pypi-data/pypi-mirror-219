# cython: language_level=3
# cython: wraparound=False
import numpy as np
cimport numpy as np
from libcpp.vector cimport vector
from libcpp.string cimport string

ctypedef long double ldouble

cdef extern from "tsp_cpp.h":
    vector[string] mst_solve(vector[string]& vertex_labels, vector[vector[ldouble]]& vertex_distances, int end)

def tsp(np.ndarray[np.float64_t, ndim=2] distances, int end=-1):
    """
    cython function to calculate tsp path with spanning tree

    :param distances: distances matrix
    :type distances: np.ndarray[np.float64_t, ndim=2]
    :param end: point in which tsp path should end. -1 means not use
    :return: list of point in order
    :rtype: np.ndarray
    """
    cdef int x, y, size, begin
    size = distances.shape[0]
    begin = 0
    cdef vector[vector[ldouble]] vertex_distances
    cdef vector[string] names = vector[string](size);

    vertex_distances.reserve(size)
    #names.reserve(size)

    for x in range(begin, size):
        names[x] = str(x).encode('UTF-8')
        vertex_distances.push_back(vector[ldouble](size))
        for y in range(size):
            vertex_distances[x][y] = <ldouble> distances[x,y]
    result = mst_solve(names, vertex_distances, end)
    res = []
    for x in range(<int> result.size()):
        res.append(int(result[x].c_str().decode('UTF-8')))
    #print(str(res[0]) + "---" + str(res[-1]))
    return np.array(res)