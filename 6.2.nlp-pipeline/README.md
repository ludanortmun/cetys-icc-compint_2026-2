# NLP Pipeline

## Introduction

In this activity, you will build a small, reusable Natural Language
Processing (NLP) pipeline for Yelp restaurant reviews. Instead of writing one
large text-processing function, you will compose small plugins with a specific
role: preprocessors transform raw text, a tokenizer produces tokens, and
postprocessors transform tokens.

Each call to the pipeline processes **one document** and produces that
document's final list of tokens. The pipeline also keeps a vocabulary across
calls. During inference, it can keep that vocabulary fixed and return
`"<unk>"` for final tokens that it has not learned.

## Setup

From this project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The `-e .` line in `requirements.txt` installs `textpipeline` in editable
mode. Therefore, changes in `src/textpipeline/` are immediately available to
the notebook. Before using the lemmatizer, call its `ensure_wordnet()` method.
It downloads the required WordNet data to a temporary directory for the current
session.

## Project structure

```
.
├── data/yelp_labelled.txt      # Yelp review corpus
├── notebooks/nlp-pipeline.ipynb
├── src/textpipeline            # Your pipeline library
├── tests                       # Automated tests for scored library behavior
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Jupyter guidelines

Use the virtual environment created above, clear notebook outputs before
committing, and do not modify existing notebook cells. Add code or markdown
cells immediately below the relevant instructions instead. The notebook is
deterministic and should run from top to bottom.

## Run and validate

Run the library tests from this activity directory:

```bash
pytest tests
```

Run the notebook as a test:

```bash
pytest --nbmake notebooks
```

Verify that its output is clear before submission:

```bash
nbstripout --verify --keep-id notebooks/nlp-pipeline.ipynb
```

The canonical validation command, run from the repository root, is:

```bash
sync-assign check 6.2
```

## Student instructions

Implement the method bodies in `src/textpipeline/`. Do not change their public
names, parameters, return types, or the three phase base classes:

- `Preprocessor`: `str -> str`
- `Tokenizer`: `str -> list[Token]`
- `Postprocessor`: `list[Token] -> list[Token]`

Each phase class is callable and must implement `display_name() -> str`.
The base classes use that stable name for their `repr`. Predefined plugin names
are part of the public contract and must not change.

All phase plugins must also handle boundary inputs consistently:

- Preprocessors raise `TypeError` for `None` or non-string input, and return
  `""` for `""`.
- Tokenizers raise `TypeError` for `None` or non-string input, and return `[]`
  for `""`.
- Postprocessors raise `TypeError` for `None` or non-list input, and return
  `[]` for `[]`.

### Part 1: Pipeline orchestration and vocabulary

Implement `TextPipeline.process`. It must apply preprocessors, then the
tokenizer, then postprocessors to exactly one document. Its return value is
the final `list[Token]` for that document.

All `TextPipeline` constructor arguments are optional. Preprocessors and
postprocessors default to empty lists, and the tokenizer defaults to a
`WordTokenizer()` instance.

`update_vocab` defaults to `False`. Pass it explicitly on every call. When it
is `True`, add every final Token to `pipeline.vocabulary`. When it is `False`,
do not modify vocabulary; replace any final Token not already present with
`Token("<unk>")`.

`repr(pipeline)` must describe its configured structure and current vocabulary
size in this format:

```text
textpipeline: {steps: {pre: (<preprocessor names>), tokenizer: (<tokenizer name>), post: (<postprocessor names>)}, vocab_size: <n>}
```

For example, `Lemmatizer(pos="v")` displays as `lemmatizer(pos=v)` and
`NGramGenerator(2)` displays as `ngram_generator(n=2)`.

### Part 2: Preprocessing and tokenization plugins

Implement the `__call__` methods of `CasingNormalizer`,
`SpecialCharacterRemover`, and `WordTokenizer`. Character removal must replace
every non-alphabetic, non-whitespace character with a space. The word tokenizer
must return only alphabetic English word Tokens.

### Part 3: Postprocessing plugins

Implement the following token-to-token-list postprocessors:

- `SimpleStemmer`: remove `ing`, `ed`, and `s` only when at least three
  characters remain after removal.
- `StopwordRemover`: remove Tokens found in the supplied `ENGLISH_STOPWORDS`
  set. Do not use an external stopword corpus.
- `Lemmatizer`: use NLTK's `WordNetLemmatizer`. Its `pos` is an instance
  property configured when constructing the plugin, such as `Lemmatizer(pos="v")`.
  Call `ensure_wordnet()` before using the plugin to download its resource to
  the temporary session directory.
- `NGramGenerator(n)`: generate arbitrary positive `n`-grams.
  Each output n-gram is one Token joining its source Tokens with `"<sep>"`,
  such as `very<sep>good`.

Use only Python standard-library modules for the pipeline except for the NLTK
lemmatizer.

### Part 4: Compose pipelines in the notebook

Complete `notebooks/nlp-pipeline.ipynb` by adding cells that compose and run
the requested pipelines over individual Yelp reviews. You will also implement
a contraction-expander `Preprocessor` in the notebook by extending its base
class. The supplied assertions check vocabulary growth, n-gram output,
POS-configured lemmatization, contraction expansion, and frozen-vocabulary
unknown handling.

### Scoring

| Component | Points |
|---|---:|
| Correct implementation of the `TextPipeline` class | 15 |
| Correct `CasingNormalizer` implementation | 5 |
| Correct `SpecialCharacterRemover` implementation | 5 |
| Correct `WordTokenizer` implementation | 5 |
| Correct `SimpleStemmer` implementation | 10 |
| Correct `StopwordRemover` implementation | 10 |
| Correct `Lemmatizer` implementation | 10 |
| Correct `NGramGenerator` implementation | 10 |
| Correct `nlp-pipeline.ipynb` compositions and interpretation | 30 |
| **Total** | **100** |
