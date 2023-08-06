"""
This is tsp_spanning module. Currently its contains :py:func:`tsp` function 
and wrappers which simplify usage on list of points

.. py:function:: tsp(np.ndarray[np.float64_t, ndim=2] distances, int end=-1)

    Function to calculate tsp path with spanning tree.
    Returned path always start with point with index 0.

    :param distances: distances matrix
    :type distances: np.ndarray[np.float64_t, ndim=2]
    :param end: point in which tsp path should end. -1 means not use
    :return: list of point in order
    :rtype: np.ndarray
"""
import numpy as np

from .tsp_wrap import tsp


# from https://stackoverflow.com/a/52030534/7475772

def ext_arrays(A,B, precision="float64"):
    nA,dim = A.shape
    A_ext = np.ones((nA,dim*3), dtype=precision)
    A_ext[:,dim:2*dim] = A
    A_ext[:,2*dim:] = A**2

    nB = B.shape[0]
    B_ext = np.ones((dim*3,nB), dtype=precision)
    B_ext[:dim] = (B**2).T
    B_ext[dim:2*dim] = -2.0*B.T
    return A_ext, B_ext


def points_to_distance_matrix(points):
    """
    This function is replacement of scipy.spatial.distance.cdist if one do not need 
    whole scipy module only for one function.

    :param np.ndarray points: points to calculate distance matrix.
    :return: distance matrix
    :rtype: np.ndarray
    """
    A_ext, B_ext = ext_arrays(points, points)
    dist = A_ext.dot(B_ext)
    np.fill_diagonal(dist,0)
    return np.sqrt(dist)


def point_tsp(points):
    """
    this function calculate distance matrix for given list of points
    then calculate tsp solution and return points in new order
    
    :param points: points to be visited
    :return: points in new order
    :rtype: np.ndarray
    """
    points = np.array(points)
    distance_matrix = points_to_distance_matrix(points)
    new_order = tsp(distance_matrix)
    return np.array([points[x] for x in new_order])
