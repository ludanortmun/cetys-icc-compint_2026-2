from pathlib import Path

# This editable package lives at ACTIVITY/src/iris_classifier/.
MODELS_DIR = Path(__file__).resolve().parents[2] / "models"
DEFAULT_MODEL_PATH = MODELS_DIR / "iris.joblib"


class IrisClassifier:
    """Load a fitted Iris estimator and classify batches of four measurements."""

    def __init__(self, model_path: str | Path = DEFAULT_MODEL_PATH):
        """Load the joblib bundle; expose its estimator as model and names as class_names."""
        raise NotImplementedError("Import model — 25 points")

    def classify(self, X) -> list[str]:
        """Return one species name per row of X, in input order; X has shape (n, 4)."""
        raise NotImplementedError("Classify — 40 points")

    def classify_with_probs(self, X) -> list[dict[str, float]]:
        """Return one {species: probability} dictionary per row, including every class."""
        raise NotImplementedError("Class probabilities — 5 extra points")
