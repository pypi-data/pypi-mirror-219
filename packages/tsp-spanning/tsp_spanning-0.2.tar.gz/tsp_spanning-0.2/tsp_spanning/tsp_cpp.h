#pragma once
#include <Python.h>
#include <algorithm>
#include <string>
#include <vector>

// approximates tsp using a minimal spanning tree (2-approximation)
// returns a permutation of the vertex_labels vector
// the first vertex of the returned vector is the first vertex of vertex_labels
// if end > -1 then end os number of vertices which should be last
std::vector<std::string> mst_solve(
    std::vector<std::string>& vertex_labels,
    std::vector<std::vector<long double>>& vertex_distances,
    int end);
