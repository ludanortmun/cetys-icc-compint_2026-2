# Text Processing

## Introduction

This assignment introduces basic text processing with Python. You will use
regular expressions and built-in Python data structures to prepare a dataset
of Yelp restaurant reviews for simple analysis.

## Setup

From this project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Jupyter guidelines

The following are a set of rules to follow when working with Jupyter
Notebooks for this course. **If any of these are not followed, then your
submission will not be valid.**

#### Use a virtual environment

Follow the setup instructions in this document before starting the Jupyter
server. If you use an IDE or editor to work with the notebook, make sure the
virtual environment's Python interpreter is selected.

#### Clear notebook outputs

Notebook outputs can often cause git conflicts. Because of this, always clear
your notebook outputs before you commit your changes.

The notebook is deterministic, so you can re-create its output by running all
cells sequentially.

#### Don't modify existing cells

You may add new cells, but you must not make changes to existing cells.

## Run and validate

The notebook includes assertions at specific cells to check your work, in a
similar way to unit tests. Run all cells sequentially to check the assertions
while you work.

The best way to validate your assignment before submission is by running this command **from the root of your repository**:

```bash
sync-assign check 6.1
```

This requires `sync-assign >= v1.0.0` ([link](https://github.com/ludanortmun/sync-assign)) and `uv` ([link](https://docs.astral.sh/uv/)) installed.

Alternatively:


To execute the notebook as a test from the project directory, run:

```bash
# Runs each notebook in notebooks/ as if it were a unit test file.
# Any execution error counts as a test failure.
pytest --nbmake notebooks
```

Before submission, verify that the notebook outputs have been cleared:

```bash
nbstripout --verify --keep-id notebooks/text-processing.ipynb
```

## Student Instructions

Complete the missing cells in
[notebooks/text-processing.ipynb](notebooks/text-processing.ipynb), following
the instructions throughout the notebook. Do not add any imports; the notebook
already imports everything needed for the assignment.

Remember to follow the [Jupyter guidelines](#jupyter-guidelines), especially
the requirements to add cells rather than modify existing ones and to clear
all outputs before submitting. **Otherwise, your submission score will be halved.**

### Scoring

| Component | Points |
|---|---:|
| Part 1: Extracting reviews | 10 |
| Part 2: Contractions | 20 |
| Part 3: Remove non-alphabetic characters | 20 |
| Part 4: Normalizing whitespace | 20 |
| Part 5: Vocabulary | 20 |
| Part 6: Reflection | 10 |
| **Total** | **100** |

