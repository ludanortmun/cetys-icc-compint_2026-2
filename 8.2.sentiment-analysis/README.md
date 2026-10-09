# 8.2 Sentiment Analysis

## Introduction

Predict whether a movie review expresses positive or negative sentiment using
the [Stanford Large Movie Review Dataset](https://ai.stanford.edu/~amaas/data/sentiment/)
(Maas et al., 2011), introduced in activity 7.1. You will implement basic text
normalization, train a supplied baseline pipeline, and design two independent
alternatives. Compare their test accuracy and use the best observed classifier
to predict sentiment for new texts.

Use scikit-learn for vectorization and logistic regression, pandas for the
dataset and comparison table, and NLTK or spaCy when useful for your chosen NLP
techniques.

## Setup

Use Python 3.14. From this activity directory, create an isolated environment:

```bash
python -m venv .venv  # or python3
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.
Open `notebooks/sentiment-analysis.ipynb` and select this environment's Python
interpreter/kernel. Both NLTK and spaCy are installed by `requirements.txt`
and available for your chosen NLP techniques.

If you use NLTK or spaCy, add your own notebook setup cells that download any
corpora or language models required by your technique **at runtime**, before
the cells that use those resources. Use `nltk.download(...)` for NLTK resources
or `spacy.cli.download(...)` for spaCy models, and document which resources
your pipeline needs. The notebook must run from top to bottom without requiring
manual corpus or model downloads beforehand. If your chosen technique needs
no downloaded resources, explain that in your notebook; NLTK stemming and
spaCy's blank English tokenizer do not require such downloads.

### Download the movie reviews

1. Download `aclImdb_v1.tar.gz` from the dataset page linked above.
2. Extract it into this activity's `data/` directory, preserving `aclImdb/`.
3. Verify that `data/aclImdb/train/pos/`, `train/neg/`, `test/pos/`, and
   `test/neg/` each contain 12,500 `.txt` reviews.

You may copy an existing complete download from activity 7.1 into this
activity's `data/` directory. Download before running the notebook. Archives,
extracted reviews, and optional NLP resources in `data/` are ignored by Git;
do not submit them. Use raw review files, not the archive's precomputed
bag-of-words features or unlabeled reviews.

## Supplied dataset and partitioning

The loader and partitioning are complete and ungraded. Keep them unchanged.
The supplied pandas DataFrames contain `review_id`, `text`, and `label`, with
`0 = negative` and `1 = positive`. Common preparation removes HTML tags before
the texts reach any of the three pipelines.

All students use the same 10,000 reviews and 80/20 partition:

- Training: 4,000 positive and 4,000 negative reviews from official `train`.
- Test: 1,000 positive and 1,000 negative reviews from official `test`.

For each official partition separately, the loader sorts filenames, uses a
fresh `random.Random(42)` to sample positive reviews and then negative reviews,
and shuffles the combined sample using that same generator. It supplies
`X_train`, `X_test`, `y_train`, and `y_test` with fixed membership and order.
Do not split again, shuffle, filter, concatenate, or replace these inputs.

Learn vocabulary, IDF, and classifier parameters only from training data.
Use each fitted pipeline's `predict(X_test)` for evaluation. Keep vectorized
matrices sparse; do not call `toarray()` or build a dense document-term matrix.

## Student instructions

Add your own code cells immediately below each implementation prompt, before
its supplied checks. Preserve all original cells, dataset variables, and
assertions. You may add imports needed by your chosen alternatives in new
cells. Keep implementations in this notebook; no Python package is required.

### 1. Baseline preprocessing — 20 points

Implement `normalize_text(text: str) -> str`:

1. Lowercase the text.
2. Replace every character other than an English letter (`a`–`z`) or whitespace
   with a space. Replace characters rather than joining words across punctuation.
3. Collapse consecutive whitespace to one space and remove leading/trailing
   whitespace.

An empty or entirely non-alphabetic text returns `""`. For example,
`"GREAT movie!!! 10/10"` becomes `"great movie"`, and `"good-bad"` becomes
`"good bad"`. This baseline does not stem, lemmatize, or remove stopwords.

### 2. Train and evaluate the supplied baseline — 25 points

After your normalizer, a supplied cell creates `baseline_pipeline`:

```python
baseline_pipeline = Pipeline([
    ("vectorizer", CountVectorizer(preprocessor=normalize_text)),
    ("classifier", LogisticRegression(max_iter=1000)),
])
```

Train this exact instance using `fit(X_train, y_train)`. Store test predictions
as `baseline_predictions` and calculate `baseline_accuracy` using
`accuracy_score(y_test, baseline_predictions)`. Display accuracy as a percentage
but keep its stored value as a fraction between zero and one.

Do not replace or reconfigure the supplied pipeline. CountVectorizer uses its
default word-count behavior, including its default token pattern (words of at
least two characters). Its custom preprocessor calls your normalizer.

### 3. Alternative 1 — 20 points

Create a new `Pipeline` instance named `alternative_1_pipeline`, fit it on the
same training inputs, and store `alternative_1_predictions` and
`alternative_1_accuracy` for the same test inputs. Add a brief markdown cell
explaining your changes and why they may affect sentiment classification.

### 4. Alternative 2 — 20 points

Create another new `Pipeline` instance named `alternative_2_pipeline`, fit it
on the same training inputs, and store `alternative_2_predictions` and
`alternative_2_accuracy`. Explain its changes in a new markdown cell.

Both alternatives must satisfy these rules:

- Each is a complete text-to-prediction pipeline with its own new vectorizer
  and its own new `LogisticRegression(max_iter=1000)` classifier. Leave other
  classifier settings at their defaults, as in the baseline.
- Name the vectorizer step `"vectorizer"` and final classifier step
  `"classifier"`. Optional preprocessing transformer steps may precede them.
- Choose `CountVectorizer` or `TfidfVectorizer`. Across the two alternatives,
  use `TfidfVectorizer` at least once.
- At least one alternative introduces an advanced technique such as stemming,
  lemmatization, or word/character n-grams. Changing counts to TF-IDF alone is
  sufficient for the other alternative.
- Each design must differ from the baseline and from the other alternative
  through preprocessing or vectorization. A different variable name or a
  different classifier setting does not count as a new design.
- Keep processing inside the pipeline or vectorizer so the same transformations
  apply automatically to training, test, and future texts.

NLTK or spaCy may support your choices. You do not need both libraries, and
an n-gram experiment can use scikit-learn directly. Explain any tokenizer,
stopword, or negation-handling decisions. Improvement over the baseline is
not required. Implement exactly these two alternatives; do not perform search,
cross-validation, or repeated tuning based on test results.

### 5. Compare and classify new texts — 15 points

Create a pandas DataFrame named `results` with columns `pipeline` and
`accuracy`. Include exactly three rows in this order: `"baseline"`,
`"alternative_1"`, and `"alternative_2"`, with their calculated accuracies.
Display the table, showing accuracies as percentages without changing the
stored fractions.

Store the name of the highest-scoring pipeline as `best_name` and that same
fitted instance as `best_pipeline`. Break ties by the table's original order.
Do not retrain on the test set or combine training and test data.

Use `best_pipeline.predict(new_texts)` on the supplied new texts and store
`new_predictions`. Display each text with its predicted sentiment. No specific
prediction is required for these examples, which have no supplied true labels.

Add a brief markdown interpretation of the three accuracies: identify the best
observed classifier, explain whether the alternatives helped, and discuss one
possible reason. Selecting a design using test accuracy is a simplified class
experiment; its winning score is not a separate, untouched final evaluation.

## Run and validate

Restart the kernel and run every cell from top to bottom. Each scored criterion
has its own assertion cell. Until you add student implementations, the starter
notebook intentionally fails at the first missing function.

From this activity directory, with the environment activated:

```bash
python -m pytest --nbmake --nbmake-timeout=600 notebooks
python -m nbstripout --keep-id notebooks/sentiment-analysis.ipynb
python -m nbstripout --verify --keep-id notebooks/sentiment-analysis.ipynb
```

From your submissions repository root, canonical validation is:

```bash
sync-assign check 8.2
```

The assertions check executable behavior, including training against the fixed
partition, calculated scores, and independent pipeline instances. Some checks
refit a copy on training data, so validation takes longer than a single fit.
Your explanations and the suitability of the advanced technique are also
reviewed by the teacher; a structural check alone cannot establish their quality.
There is no minimum accuracy requirement.

## Scoring and submission

| Component | Points |
|---|---:|
| Baseline preprocessing | 20 |
| Supplied baseline: training, predictions, and accuracy | 25 |
| Alternative 1: independent design, training, and evaluation | 20 |
| Alternative 2: independent design, training, and evaluation | 20 |
| Comparison, best classifier selection, and new-text predictions | 15 |
| **Total** | **100** |

Submit the completed notebook with cleared outputs in `8.2.sentiment-analysis`.
Use an isolated virtual environment, retain the fixed random seed, and preserve
all supplied notebook cells. Follow the course's Jupyter guidelines; failure
to follow them halves the total score. Do not submit environments, datasets,
or downloaded NLP resources.
