import numpy as np
from iris_classifier import IrisClassifier
from iris_classifier.classifier import DEFAULT_MODEL_PATH


def test_loads_bundle_from_disk(bundle, monkeypatch, tmp_path):
    path, model, names, X = bundle
    monkeypatch.chdir(tmp_path)
    classifier = IrisClassifier(path)
    assert classifier.class_names == names
    assert classifier.model is not model
    np.testing.assert_array_equal(classifier.model.predict(X), model.predict(X))
    np.testing.assert_array_equal(classifier.model.classes_, model.classes_)


def test_default_path_is_activity_models_directory():
    assert DEFAULT_MODEL_PATH.parent.name == "models"
    assert (DEFAULT_MODEL_PATH.parent.parent / "src").is_dir()
