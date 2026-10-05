# 8.1 Classification

## Introduction

Build a classifier that predicts an Iris flower's species from four measurements in centimeters: sepal length, sepal width, petal length, and petal width. The [Iris dataset included in scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html) contains 150 flowers, four numeric features, and three classes (50 flowers each): `0 = setosa`, `1 = versicolor`, `2 = virginica`. No dataset download is required.

Use only an 80/20 train/test split, `LogisticRegression`, and accuracy. The supplied notebook loads the dataset and imports the required tools. All student implementation belongs in **new code cells immediately after the three marked instruction cells**. Preserve the supplied cells, original `X` and `y`, and assertions. No Python package or additional files need to be implemented.

## Setup

Use Python 3.14. From this activity directory:

```bash
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
uv run --python .venv/bin/python --no-project jupyter lab
```

Open `notebooks/classification.ipynb` and select the activity environment's Python kernel.

## Student instructions

### 1. Split the dataset — 30 points

Call `train_test_split` with `X` and `y` together, `test_size=0.20`, and `random_state=42`. Leave other arguments at their defaults. Store the results as `X_train`, `X_test`, `y_train`, and `y_test` in that return order.

The training set must contain 120 rows and the test set 30 rows, each with all four original features. Each feature row must remain paired with its correct label. Do not alter, reorder, or filter the supplied dataset before splitting.

### 2. Train the classifier — 40 points

Create `model` as a `LogisticRegression(max_iter=1000)` instance, leaving other arguments at their defaults. Train it with `X_train` and `y_train` using `fit`. Do not use any test rows or labels for training. The higher iteration limit lets this example finish fitting without changing the input measurements.

### 3. Predict and calculate accuracy — 30 points

Use the trained model's `predict` method on `X_test`, storing the returned array as `predictions`. Compute `accuracy` using `accuracy_score(y_test, predictions)` with default arguments. This is a fraction between zero and one, not a percentage or a count. Display it as a percentage using a print statement.

Accuracy is the number of correct test predictions divided by the number of test examples. Calculate it from your predictions; do not hardcode predictions or a score. You are graded on correct prediction and evaluation, not on achieving a minimum accuracy.

### Supplied demonstration

After the three steps, the notebook uses the trained model to classify one flower and displays its predicted species. Its row contains the four measurements in the original feature order. This demonstration is complete and carries no additional points.

## Run and validate

Restart the kernel and run every cell from top to bottom. Each scored step has its own assertion cell. The unfinished template intentionally fails at the first missing student variable.

From this activity directory:

```bash
uv run --python .venv/bin/python --no-project pytest --nbmake notebooks
uv run --python .venv/bin/python --no-project nbstripout notebooks/classification.ipynb
uv run --python .venv/bin/python --no-project nbstripout --verify --keep-id notebooks/classification.ipynb
```

From your submissions repository root, canonical validation is:

```bash
sync-assign check 8.1
```

## Scoring and submission

| Component | Points |
|---|---:|
| Correct paired 80/20 split with the specified seed | 30 |
| LogisticRegression fitted only on the training set | 40 |
| Test predictions and calculated accuracy | 30 |
| **Total** | **100** |

Each criterion requires all of its assertions to pass. Submit the notebook with your new implementation cells and cleared outputs in `8.1.classification`. Do not modify the supplied instructions, dataset loading, checks, or demonstration.
