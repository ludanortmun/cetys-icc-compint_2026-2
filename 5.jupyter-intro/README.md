# Jupyter Intro

## Introduction

This assignment is intended to help you get familiar with the guidelines for Jupyter Notebook usage for this course.

## Setup

From this project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Quick note on requirements.txt

If you read the contents of [requirements.txt](requirements.txt) you will notice that the first dependency to install is `-e .`. This is equivalent to running `pip install -e .`, which would install the package from the current directory (as defined by [pyproject.toml](pyproject.toml)) in editable mode. 

When a package is installed in editable mode, any changes made to its source would immediately be available to all modules importing it. In this case, the intention is to import the diceroll package into the Jupyter Notebook.

In this project, [requirements.txt](requirements.txt) should only include the dependencies needed to run the Jupyter Notebooks, which include the diceroll package. Note that any dependencies from the package itself are defined in [pyproject.toml](pyproject.toml), which are then resolved when installing it.

## Project structure

Since this project includes a code library (along with its own unit tests) and Jupyter Notebooks, the following structure is laid out to help organize it.

```
.
├── notebooks <------------- All Jupyter notebooks should live here
│   └── roller.ipynb
├── src <------------------- Code to be imported into the notebook
│   └── diceroll
│       ├── __init__.py
│       └── dice.py
├── tests <----------------- Unit test for the library
│  └── diceroll
│       └── test_dice.py
├── pyproject.toml <-------- Ensures the code can be installed for use with the notebook
├── README.md
└── requirements.txt
```

This will be the expected structure for any future assignment involving library and notebook code.

## Jupyter guidelines

The following are a set of rules to follow when working with Jupyter Notebooks for this course. **If any of these are not followed, then your submission will not be valid.**

#### Use a virtual environment

Follow the instructions provided in this document to setup a virtual environment before starting the Jupyter server. If you use your IDE/editor to work with the notebook, make sure the virtual environment's Python interpreter is selected.

#### Use a random seed

Very often, code with a randomness factor is executed inside a notebook. To ensure reproducibility of your submissions, always define a static random seed to be passed as argument to any method with random behavior.

If you implement a function with randomness, always accept a random seed parameter.

#### Clear notebook outputs

Notebook outputs can often cause git conflicts. Because of this, always clear your notebook outputs before you commit your changes. 

Since code is deterministic (see prior point on random seed), it's easy to re-create the exact same output by running all cells sequentially.

#### Don't modify existing cells

While you are free to add new cells, you must not make any changes to the existing cells.

## Run and validate

Run tests for the library implementation with:

```bash
# Will run all unit tests under the tests/ directory
pytest tests
```

Notebooks will include assertions at specific cells to check for correctness, in a similar way that unit tests do. To run these checks, run:

```bash
# Will run each notebook in notebooks/ directory as if they were a unit test file
# Any execution error raised would count as a test failure.
pytest --nbmake notebooks
```


As mentioned previously, all notebooks must have their output cleared before submission. This can be checked with:

```bash
# Note that this command must be run individually for each notebook file
nbstripout --verify --keep-id notebooks/roller.ipynb
```

## Student Instructions

Your implementation belongs in `src/diceroll/dice.py` and
`notebooks/roller.ipynb`. Do not change the public function signatures in
`dice.py`.

### Part 1: Rolling a single die

Implement `roll_d6` in `src/diceroll/dice.py`. It must return a random
integer between 1 and 6 (inclusive), simulating the roll of a six-sided
die.

If a `seed` is provided, the result must be deterministic for that seed.
Calling `roll_d6` must not mutate the global `random` module state, so any
random number generator you use must be scoped to the function call.

Hint: investigate how to use the built-in [Random](https://docs.python.org/3/library/random.html#random.Random) class.

Check your implementation with:

```bash
pytest tests/diceroll/test_dice.py
```

### Part 2: Completing the notebook

Complete the missing cells in `notebooks/roller.ipynb`, following the
instructions given throughout the notebook. This includes writing code
cells that use `dice.roll_d6`, as well as answering the reflection
questions in their corresponding markdown cells.

Remember to follow the [Jupyter guidelines](#jupyter-guidelines) described
above, including using a random seed and clearing all outputs before
submitting.

Check your implementation with:

```bash
pytest --nbmake notebooks
```

### Extra credit: Rolling multiple dice

Implement `roll` in `src/diceroll/dice.py`. It must simulate rolling a
die with `d` sides, `n` times, returning the sum of all rolls. All rolls
within a single call must use the same random number generator, optionally
seeded with the provided `seed`.

It must raise a `ValueError` if `d` is less than 2, or if `n` is less than
1. As with `roll_d6`, it must not mutate the global `random` module state.

Check your implementation with:

```bash
pytest tests/diceroll/test_dice_extra_credit.py
```

### Scoring

| Component            |  Points |
|-----------------------|--------:|
| `roll_d6`             |      50 |
| `roller.ipynb`        |      50 |
| `roll` (extra credit) |      10 |
| **Total**             | **110** |

