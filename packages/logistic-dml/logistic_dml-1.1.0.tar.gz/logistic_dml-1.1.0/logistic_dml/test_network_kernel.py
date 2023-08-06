import numpy as np

edge_list = np.array([[0, 1], [1, 2], [0, 2]])

node_kernel = np.array([[1, 2, 3],
                        [2, 3, 4],
                        [3, 4, 5]])

def f(k, x1, x2):
    return (k[x1[0], x2[0]]*k[x1[1], x2[1]]
            + k[x1[0], x2[1]]*k[x1[1], x2[0]])

def fill_in_edge_kernel(node_kernel, edge_list):
    n = edge_list.shape[0]
    edge_kernel = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            edge_kernel[i, j] = f(node_kernel, edge_list[i], edge_list[j])
    return edge_kernel

print(fill_in_edge_kernel(node_kernel, edge_list))


