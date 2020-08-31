from graph import Graph

def earliest_ancestor(ancestors, starting_node):
    gr = Graph()

    # Populate graph
    for i in ancestors:
        gr.add_vertex(i[0])
        gr.add_vertex(i[1])

        # Reverse edges for ease of traversal
        gr.add_edge(i[1], i[0])

    earliest = starting_node

    # If last node, return -1
    if len(gr.get_neighbors(earliest)) == 0:
        return -1

    while len(gr.get_neighbors(earliest)) > 0:
        next = gr.get_neighbors(earliest)
        earliest = min(list(next))

    return earliest

if __name__ == '__main__':
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    earliest_ancestor(test_ancestors, 8)
