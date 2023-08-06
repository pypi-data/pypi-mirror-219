import unittest

import numpy as np

from tsp_spanning import tsp, point_tsp, points_to_distance_matrix

class TestTSP(unittest.TestCase):
    def test_work_point(self):
        points = [(0, 0), (1, 1), (-1, -1), (1, 0)]
        res = point_tsp(points)
        self.assertTrue(len(res) == 4)
        self.assertTrue(set(points) == set(map(tuple,res)))
    
    def test_work_point_3d(self):
        points = [(0, 0, 0), (1, 1, 1), (-1, -1, -1), (1, 0, 0)]
        res = point_tsp(points)
        self.assertTrue(len(res) == 4)
        self.assertTrue(set(points) == set(map(tuple,res)))

    def test_work_tsp(self):
        points = np.array([(0, 0), (1, 1), (-1, -1), (1, 0)])
        distances = points_to_distance_matrix(points)
        self.assertTrue(distances.shape == (4,4))
        points_order = tsp(distances)
        self.assertTrue(len(points_order) == 4)

    def test_work_tsp_end(self):
        points = np.array([(0, 0), (1, 1), (-1, -1), (1, 0)])
        distances = points_to_distance_matrix(points)
        points_order = tsp(distances, 1)
        self.assertTrue(points_order[-1] == 1)


if __name__ == "__main__":
    unittest.main()
