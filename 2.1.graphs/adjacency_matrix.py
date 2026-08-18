def linear_graph_adjacency_matrix() -> list[list[bool]]:
    """
    Returns the adjacency matrix representation of the following linear graph:
    0 ─── 1 ─── 2 
    """
    pass

def branching_graph_adjacency_matrix() -> list[list[bool]]:
    """
    Returns the adjacency matrix representation of the following branching graph:
          1
          │
    0 ─── 2 ─── 3
          │
          4
    """
    pass


def cycle_graph_adjacency_matrix() -> list[list[bool]]:
    """
    Returns the adjacency matrix representation of the following cycle graph:
    0 ─── 1
    │     │
    3 ─── 2
    """
    pass

def edge_exists(adjacency_matrix: list[list[bool]], from_node: int, to_node: int) -> bool:
    """
    Returns True if there is an edge between from_node and to_node in the given adjacency matrix.
    """
    pass

def get_neighbors(adjacency_matrix: list[list[bool]], node: int) -> list[int]:
    """
    Returns a list of neighbors for the given node in the adjacency matrix.
    """
    pass