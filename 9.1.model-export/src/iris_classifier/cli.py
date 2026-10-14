from pathlib import Path
import click
from .classifier import DEFAULT_MODEL_PATH, IrisClassifier


@click.command()
@click.argument("measurements", nargs=4, type=float, metavar="CM CM CM CM")
@click.option(
    "--model", "model_path",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    default=DEFAULT_MODEL_PATH,
    show_default=True,
    help="Path to iris.joblib.",
)
def main(measurements, model_path):
    """Predict an Iris species from four measurements in centimeters.

    Order: sepal length, sepal width, petal length, petal width.
    """
    classifier = IrisClassifier(model_path)
    click.echo(classifier.classify([measurements])[0])


if __name__ == "__main__":
    main()
