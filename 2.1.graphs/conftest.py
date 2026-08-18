from pathlib import Path

import joblib
import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def expected():
    """
    Loads the expected graph representations (adjacency matrices and lists)
    used to validate the graphs you hardcode in adjacency_matrix.py and
    adjacency_list.py, as well as to independently exercise edge_exists()
    and get_neighbors().
    """
    return joblib.load(FIXTURES_DIR / "expected_graphs.joblib")
