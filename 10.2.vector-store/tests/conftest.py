import numpy as np
import pytest


class FakeEncoder:
    """Non-unit vectors expose dot-product implementations; no downloads."""

    vectors = {
        "east": [2., 0., 0.], "east copy": [7., 0., 0.],
        "diagonal": [3., 4., 0.], "north": [0., 5., 0.],
        "west": [-8., 0., 0.], "zero": [0., 0., 0.],
        "query": [4., 0., 0.], "unicode café 🐈": [0., 0., 2.],
        "almost east": [1., 0.0001, 0.],
    }

    def __init__(self):
        self.calls = []

    def encode(self, sentences, *, convert_to_numpy=True, normalize_embeddings=False):
        assert isinstance(sentences, list)
        assert convert_to_numpy is True and normalize_embeddings is False
        self.calls.append(list(sentences))
        return np.asarray([self.vectors[text] for text in sentences], dtype=float)


@pytest.fixture
def model():
    return FakeEncoder()
