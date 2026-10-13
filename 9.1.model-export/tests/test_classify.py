import numpy as np
from iris_classifier import IrisClassifier


def test_classify_maps_model_predictions_and_preserves_order(bundle):
    path, model, names, X = bundle
    classifier = IrisClassifier.__new__(IrisClassifier)
    classifier.model = model
    classifier.class_names = names
    # Isolate classification from the separately graded constructor.
    for rows in (X[::-1], X[[0, 60, 120]], X[[80]]):
        expected = [names[int(label)] for label in model.predict(rows)]
        assert classifier.classify(rows.tolist()) == expected
        assert classifier.classify(np.asarray(rows)) == expected
