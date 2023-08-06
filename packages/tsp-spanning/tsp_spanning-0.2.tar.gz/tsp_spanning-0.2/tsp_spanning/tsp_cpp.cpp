#include "tsp_cpp.h"
#include <stack>
#include <algorithm>
#include <iostream>

using EDGE = std::pair<int32_t, int32_t>;

class SolverMST
{
private:
    class UnionFind
    {
    private:
        int32_t* representants;
    public:
        UnionFind(int32_t size)
        {
            representants = new int32_t[size];
            for (int32_t i = 0; i < size; ++i)
                representants[i] = i;
        }
        ~UnionFind()
        {
            delete[] representants;
        }
        int32_t find(int32_t v)
        {
            if (representants[v] == v)
                return v;
            return representants[v] = find(representants[v]);
        }
        void merge(int32_t a, int32_t b)
        {
            a = find(a);
            b = find(b);
            representants[a] = b;
        }
    };

    std::vector<std::string>& vertex_labels;
    std::vector<std::vector<long double>>& vertex_distances;
    int end;

    void create_result_o(
        std::vector<std::vector<int32_t>>& neighbours,
        int32_t v,
        int32_t parent,
        std::vector<std::string>& result)
    {
        result.push_back(vertex_labels[v]);
        for (int32_t u: neighbours[v])
            if (u != parent)
            {
                create_result(neighbours, u, v, result);
                // result.push_back(vertex_labels[v]);
            }
    }
    void create_result(
        std::vector<std::vector<int32_t>>& neighbours,
        int32_t v,
        int32_t parent,
        std::vector<std::string>& result)
    {

        result.push_back(vertex_labels[v]);
        for (int32_t u: neighbours[v])
            if (u != parent)
            {
                create_result(neighbours, u, v, result);
                // result.push_back(vertex_labels[v]);
            }
    }

    int64_t calculate_depth(std::vector<std::vector<int32_t>>& neighbours,
        int32_t v,
        int32_t parent,
        std::vector<int64_t> & depth)
    {
        int64_t max_depth = depth[v];
        for (int32_t u: neighbours[v])
            if (u != parent)
            {
                depth[u] = calculate_depth(neighbours, u, v, depth);
                max_depth = std::max(max_depth, depth[u]);
                // result.push_back(vertex_labels[v]);
            }
        return max_depth ? max_depth + 1 : max_depth;
    }

public:
    SolverMST(
        std::vector<std::string>& _vertex_labels,
        std::vector<std::vector<long double>>& _vertex_distances, int end)
    : vertex_labels(_vertex_labels)
    , vertex_distances(_vertex_distances),
    end(end)
    {}

    std::vector<std::string> solve()
    {

        int32_t num_of_vertices = vertex_labels.size();
        std::vector<EDGE> edges;
        for (int32_t i = 0; i < num_of_vertices; ++i)
            for (int32_t j = i + 1; j < num_of_vertices; ++j)
                edges.emplace_back(i, j);

        std::sort(edges.begin(), edges.end(),
            [this](EDGE e1, EDGE e2)
            {
                return this->vertex_distances[e1.first][e1.second] < 
                    this->vertex_distances[e2.first][e2.second];
            }
        );

        std::vector<EDGE> mst_edges;
        UnionFind components(num_of_vertices);
        for (EDGE& e: edges)
            if (components.find(e.first) != components.find(e.second))
            {
                components.merge(e.first, e.second);
                mst_edges.push_back(e);
            }

        std::vector<std::vector<int32_t>> neighbours(
            num_of_vertices,
            std::vector<int32_t>());
        for (EDGE& e: mst_edges)
        {
            neighbours[e.first].push_back(e.second);
            neighbours[e.second].push_back(e.first);
        }

        std::vector<int64_t> depth(num_of_vertices, 0);
        if (this->end > -1)
            depth[end] = num_of_vertices;
        calculate_depth(neighbours, 0, 0, depth);

        for (int32_t i = 0; i < num_of_vertices; ++i)
            std::sort(neighbours[i].begin(), neighbours[i].end(),
            [depth](int32_t e1, int32_t e2)
            {
                return depth[e1] < depth[e2];
            }
            );
        /*for (int32_t i = 0; i < num_of_vertices; ++i)
            std::cout << depth[i] << " ";
        std::cout << " ---- " <<  end  << std::endl;
        for (int32_t i = 0; i < num_of_vertices; ++i){
            if (neighbours[i].size() == 0)
                continue;
            std::cout<< i << "[" << depth[i] << "]: ";
            for(int32_t j: neighbours[i])
                 std::cout << j << ":" << depth[j] << " ";
            std::cout << std::endl;

        }*/


        std::vector<std::string> result;
        create_result(neighbours, 0, 0, result);

        return result;
    }
};

std::vector<std::string> mst_solve(
    std::vector<std::string>& vertex_labels,
    std::vector<std::vector<long double>>& vertex_distances,
    int end)
{
    SolverMST solver(vertex_labels, vertex_distances, end);
    return solver.solve();
}
