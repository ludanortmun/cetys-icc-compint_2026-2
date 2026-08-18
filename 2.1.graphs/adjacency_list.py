def linear_graph_adjacency_list() -> list[list[int]]:
    """
    Returns the adjacency list representation of the following linear graph:
    0 ─── 1 ─── 2 
    """
    pass

def branching_graph_adjacency_list() -> list[list[int]]:
    """
    Returns the adjacency list representation of the following branching graph:
          1
          │
    0 ─── 2 ─── 3
          │
          4
    """
    pass

def cycle_graph_adjacency_list() -> list[list[int]]:
    """
    Returns the adjacency list representation of the following cycle graph:
    0 ─── 1
    │     │
    3 ─── 2
    """
    pass

def edge_exists(adjacency_list: list[list[int]], from_node: int, to_node: int) -> bool:
    """
    Returns True if there is an edge between from_node and to_node in the given adjacency list.
    """
    pass

def get_neighbors(adjacency_list: list[list[int]], node: int) -> list[int]:
    """
    Returns a list of neighbors for the given node in the adjacency list.
    """
    pass