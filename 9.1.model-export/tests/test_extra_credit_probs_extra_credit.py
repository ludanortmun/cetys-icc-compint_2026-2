import numpy as np
from iris_classifier import IrisClassifier


def test_classify_with_probs_matches_estimator(bundle):
    _, model, names, X = bundle
    classifier = IrisClassifier.__new__(IrisClassifier)
    classifier.model = model
    classifier.class_names = names
    rows = X[[0, 60, 120, 80]]
    result = classifier.classify_with_probs(rows.tolist())
    assert isinstance(result, list) and len(result) == len(rows)
    expected = model.predict_proba(rows)
    for actual, probabilities in zip(result, expected):
        assert set(actual) == set(names)
        np.testing.assert_allclose([actual[names[int(c)]] for c in model.classes_], probabilities)
        assert all(0 <= p <= 1 for p in actual.values())
        assert np.isclose(sum(actual.values()), 1)
