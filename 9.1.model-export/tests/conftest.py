import joblib
import pytest
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier


@pytest.fixture
def bundle(tmp_path):
    iris = load_iris()
    model = DecisionTreeClassifier(random_state=42, max_depth=3).fit(iris.data, iris.target)
    # Deliberately nonstandard names catch hardcoded species mappings.
    names = ["species-a", "species-b", "species-c"]
    path = tmp_path / "different-model.joblib"
    joblib.dump({"model": model, "class_names": names}, path)
    return path, model, names, iris.data

