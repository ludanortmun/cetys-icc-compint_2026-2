# 9.1 Export an Iris model

Train an Iris species classifier, serialize it, and use it from the supplied
console application. The dataset and train/test split are supplied. No EDA or
preprocessing is required. Implement the notebook training/export steps and
`IrisClassifier` in the editable Python library.

## Setup

Use **Python 3.14** for both serialization and deserialization. Keep the exact
library versions in `requirements.txt` in both environments; joblib model files
require matching software versions. Versions were checked against PyPI on
2026-10-13. If you import another third-party library, add its latest stable
version as an exact `==` pin and use that same version when loading the model.
The editable activity package (`-e .`) is supplied locally.

From this activity directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, activate with `.venv\Scripts\activate`. Select this environment's
kernel. Iris is bundled with scikit-learn; no dataset download is needed.

## Layout and supplied code

- `notebooks/model-export.ipynb`: base training and joblib export.
- `notebooks/model-export_extra_credit.ipynb`: optional ONNX export. Its supplied
  setup loads the already exported `models/iris.joblib`; it does not retrain.
- `src/iris_classifier/`: editable package, student class, and complete console app.
- `models/`: serialized model files, sibling to `src` and `notebooks`.
- `extra_src/`: optional application for another language/runtime.
- `tests/`: teacher tests; preserve them unchanged.

Add your own code cells after each implementation prompt, before its assertions.
Preserve original cells, IDs, and assertions. Keep the supplied 80/20 stratified
Iris split with `random_state=42` unchanged. Feature order is **sepal length,
sepal width, petal length, petal width**, all in centimeters.

## Required work — 100 points

1. **Train and evaluate (10).** Create
   `model = LogisticRegression(max_iter=1000, random_state=42)`; fit only on
   `X_train, y_train`. Keep all other estimator settings at their defaults.
   Store `test_predictions` and `test_accuracy`, calculated with `accuracy_score`
   on the supplied test set, and display the accuracy. No minimum accuracy is
   required. Use this same fitted LogisticRegression model for joblib export and
   optional ONNX export; it also supports the probabilities extension.
2. **Export (25).** In the base notebook, use joblib to save `models/iris.joblib`
   as `{"model": model, "class_names": class_names}`. Names are `setosa`,
   `versicolor`, `virginica`, indexed by numeric labels 0, 1, 2. Preserve the
   fitted estimator. Upload this exact file to Google Drive and add an accessible
   download/share link in a new markdown cell in the base notebook. The teacher
   verifies access and the downloaded model. **The assignment is invalid without
   the Google Drive upload**, even if the model is committed to GitHub.
3. **Import (25).** Implement `IrisClassifier.__init__` in
   `src/iris_classifier/classifier.py`. Load the joblib dictionary from
   `model_path`; expose the estimator as `self.model` and species list as
   `self.class_names`. The supplied default is the activity's `models/iris.joblib`
   and works independently of the current directory. Honor explicit paths;
   do not train or substitute a model when loading.
4. **Classify (40).** Implement `IrisClassifier.classify(X) -> list[str]`.
   `X` is a numeric list of rows or NumPy array of shape `(n, 4)`, with `n >= 1`.
   Use the loaded estimator's predictions and map numeric labels through
   `self.class_names`. Return one species name per row, preserving input order.
   A single sample is still a matrix, for example `[[5.1, 3.5, 1.4, 0.2]]`.
   Input validation beyond this contract is not scored. The console app is
   supplied and calls this method; leave it as the application scaffold.

## Optional work — 20 extra points

- **Probabilities (5).** Implement `classify_with_probs(X)` in the same class.
  Return a list of dictionaries, one per input row: each dictionary contains all
  class names mapped to their probabilities as floats. Align `predict_proba`
  columns using the loaded estimator's `classes_`; each row sums to one.
- **ONNX export (5).** In the separate `model-export_extra_credit.ipynb`, convert
  the already loaded estimator using skl2onnx and write `models/iris.onnx`.
  Follow the notebook's float32 `(n, 4)` input, `label` output, and `class_names`
  metadata contract. Convert the same LogisticRegression estimator, disable ZipMap, and verify that
  the ONNX predictions match the joblib model. The supplied assertions use ONNX's
  reference evaluator, so Python ONNX Runtime is not required.
- **ONNX import and prediction in another runtime (10).** Implement the equivalent
  batch-to-species functionality in a language/platform of your choice, different
  from the base Python/scikit-learn environment (for example Node.js, Java, C#,
  or a browser). Put the complete project in `extra_src/`, with its own
  `extra_src/README.md` documenting dependencies, setup, compilation where
  applicable, and running instructions. Missing usable instructions invalidates
  this criterion. Read the actual `models/iris.onnx` for inference and map labels
  to species. Do not retrain or delegate inference to the Python application.
  Complete the supplied README template with your project's actual instructions
  and an example prediction. You may choose the application's interface and
  input/output format. The teacher manually grades model loading, prediction,
  runtime choice, and setup reproducibility; there is no automated runtime test.

## Run and validate

Run the base notebook first, top to bottom, to create the model. Run the optional
notebook next if attempting ONNX. Then try the supplied console application:

```bash
python -m iris_classifier.cli 5.1 3.5 1.4 0.2
python -m iris_classifier.cli --model models/iris.joblib 6.7 3.0 5.2 2.3
python -m pytest --nbmake notebooks/model-export.ipynb
python -m pytest tests/test_import_model.py tests/test_classify.py
```

To validate ONNX export and class probabilities:

```bash
python -m pytest --nbmake notebooks/model-export_extra_credit.ipynb
python -m pytest tests/test_extra_credit_probs_extra_credit.py
```

Clear saved outputs before submission, preserving cell IDs:

```bash
python -m nbstripout --keep-id notebooks/*.ipynb
python -m nbstripout --verify --keep-id notebooks/*.ipynb
```

From the submissions repository root, canonical validation is:

```bash
sync-assign check 9.1
```

The starter intentionally fails until students implement the scored work.
Optional checks may fail when the extension is not attempted; sync-assign treats
these as nonblocking. Extra-credit test filenames use both the course's
`test_extra_credit_` prefix and sync-assign's `_extra_credit.py` suffix.
Notebook assertions verify executable behavior, and Python tests isolate import,
classification, and probabilities. The teacher also reviews training on the
supplied split, Google Drive access, use of a genuinely different ONNX runtime,
and its documented clean setup.

## Scoring and submission

| Component | Points |
|---|---:|
| Iris model training and test accuracy — base notebook | 10 |
| Joblib export — base notebook | 25 |
| Joblib import — Python library | 25 |
| `IrisClassifier.classify` — Python library | 40 |
| **Base total** | **100** |
| `IrisClassifier.classify_with_probs` — Python library | +5 |
| ONNX export — separate extra-credit notebook | +5 |
| ONNX import and prediction — different runtime in `extra_src` | +10 |
| **Maximum** | **120** |

Submit the activity in your course repository, including completed notebooks
with cleared outputs, library code, and Google Drive share link. Serialized
models may be committed to GitHub. For ONNX runtime credit, include the complete
`extra_src` project and its actual README. Do not submit virtual environments,
installed runtime dependencies, or build artifacts. Follow course Jupyter
conventions; failure to follow them halves the total score.
