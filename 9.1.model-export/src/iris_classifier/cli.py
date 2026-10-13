import argparse
from .classifier import DEFAULT_MODEL_PATH, IrisClassifier


def main():
    parser = argparse.ArgumentParser(description="Predict an Iris species from measurements in cm.")
    parser.add_argument("measurements", nargs=4, type=float,
                        metavar="CM", help="sepal length, sepal width, petal length, petal width")
    parser.add_argument("--model", default=str(DEFAULT_MODEL_PATH), help="Path to iris.joblib")
    args = parser.parse_args()
    classifier = IrisClassifier(args.model)
    print(classifier.classify([args.measurements])[0])


if __name__ == "__main__":
    main()
